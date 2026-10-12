"""
Автоматические тесты для сценария open-redirect.

Библиотека тестирования: pytest.
Проверяют, что сервер авторизации уязвим к открытому перенаправлению
и что обмен кода на токен работает.
"""
import requests

BASE = "http://localhost:8080"


def test_open_redirect():
    """
    Проверяет, что сервер перенаправляет на произвольный redirect_uri.

    Отправляет запрос с вредоносным redirect_uri и проверяет,
    что в заголовке Location возвращается именно этот адрес.
    """
    malicious = "http://evil.example.com/steal"
    r = requests.get(
        f"{BASE}/authorize",
        params={
            "client_id": "test-client",
            "redirect_uri": malicious,
            "response_type": "code",
            "state": "test",
        },
        allow_redirects=False,
    )
    assert r.status_code == 302
    assert malicious in r.headers.get("Location", "")


def test_token_exchange():
    """
    Проверяет, что обмен кода на токен работает.

    Сначала получает код через /authorize, извлекает его из Location,
    затем отправляет на /token и проверяет наличие access_token в ответе.
    """
    r = requests.get(
        f"{BASE}/authorize",
        params={
            "client_id": "test-client",
            "redirect_uri": "http://localhost:8081/callback",
            "response_type": "code",
            "state": "test",
        },
        allow_redirects=False,
    )
    loc = r.headers.get("Location", "")
    code = loc.split("code=")[1].split("&")[0]

    t = requests.post(
        f"{BASE}/token",
        data={"code": code, "grant_type": "authorization_code"},
    )
    assert t.status_code == 200
    assert "access_token" in t.json()