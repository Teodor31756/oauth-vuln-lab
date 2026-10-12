"""
Клиентское приложение OAuth.

Инициирует поток Authorization Code Grant:
перенаправляет пользователя на сервер авторизации,
принимает обратный вызов с кодом и обменивает его на токен.

Входные данные:
    GET /          — старт авторизации
    GET /callback  — обратный вызов с параметрами code и state

Выходные данные:
    HTML-страница с токеном доступа или сообщением об ошибке
"""
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

AUTH = 'http://auth-server:8080'
CLIENT_ID = 'test-client'
CLIENT_SECRET = 'test-secret'
REDIRECT_URI = 'http://localhost:8081/callback'


@app.route('/')
def index():
    """
    Инициирует OAuth-поток.

    Формирует URL сервера авторизации с параметрами client_id,
    redirect_uri, response_type=code и state, затем перенаправляет браузер.

    Возвращает: HTTP 302 (redirect) на сервер авторизации.
    """
    url = (
        f"{AUTH}/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&state=abc123"
    )
    return redirect(url)


@app.route('/callback')
def callback():
    """
    Обрабатывает обратный вызов от сервера авторизации.

    Принимает code из параметров запроса, обменивает его на токен
    через POST-запрос к /token сервера авторизации.

    Возвращает: строку с access_token при успехе, иначе текст ошибки и HTTP 400.
    """
    code = request.args.get('code')
    r = requests.post(
        f"{AUTH}/token",
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    if r.status_code == 200:
        return f"access_token: {r.json()['access_token']}"
    return r.text, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)