"""
Уязвимый сервер авторизации OAuth 2.0.

Демонстрирует уязвимость открытого перенаправления (CWE-601):
значение redirect_uri не проверяется по списку разрешённых адресов,
что позволяет злоумышленнику перехватить авторизационный код.

Входные данные:
    GET /authorize?client_id=...&redirect_uri=...&response_type=code&state=...
    POST /token с form-data: code, grant_type

Выходные данные:
    HTTP 302 с заголовком Location, содержащим code и state
    JSON с полем access_token или error
"""
from flask import Flask, request, redirect, jsonify
import uuid

app = Flask(__name__)

# Хранилище выданных авторизационных кодов.
# Ключ — код, значение — словарь с client_id, redirect_uri, state.
codes = {}


@app.route('/authorize')
def authorize():
    """
    Конечная точка авторизации.

    Принимает client_id, redirect_uri, response_type, state.
    Генерирует авторизационный код и перенаправляет браузер
    на redirect_uri, передавая код и state в параметрах запроса.

    УЯЗВИМОСТЬ: redirect_uri не проверяется по белому списку,
    поэтому перенаправление возможно на любой адрес.

    Возвращает: HTTP 302 (redirect).
    """
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state', '')

    code = str(uuid.uuid4())
    codes[code] = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
    }

    # УЯЗВИМОСТЬ: redirect_uri берётся из запроса без проверки.
    # Корректная реализация должна сверить redirect_uri с белым списком.
    return redirect(f"{redirect_uri}?code={code}&state={state}")


@app.route('/token', methods=['POST'])
def token():
    """
    Конечная точка обмена авторизационного кода на токен доступа.

    Принимает code и grant_type.
    Проверяет наличие кода в хранилище, удаляет его и возвращает
    фиктивный access_token.

    Возвращает: JSON с access_token при успехе, JSON с error и HTTP 400 иначе.
    """
    code = request.form.get('code')
    if code in codes:
        codes.pop(code)
        return jsonify({
            'access_token': f"token-{uuid.uuid4()}",
            'token_type': 'Bearer',
            'expires_in': 3600,
        })
    return jsonify({'error': 'invalid_grant'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)