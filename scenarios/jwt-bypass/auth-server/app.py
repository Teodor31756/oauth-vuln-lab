"""
Уязвимый сервер проверки JWT.

Демонстрирует уязвимость обхода проверки подписи (CWE-347):
токен декодируется с параметром verify_signature=False,
что позволяет подделать его содержимое.

Входные данные:
    POST /verify с JSON: {"token": "<jwt>"}
    POST /admin  с JSON: {"token": "<jwt>"}

Выходные данные:
    JSON с полями valid, claims или error
    JSON с полями welcome, user, role или error
"""
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)


@app.route('/verify', methods=['POST'])
def verify():
    """
    Проверка валидности JWT.

    Принимает токен из тела запроса, декодирует его без проверки подписи.

    УЯЗВИМОСТЬ: verify_signature=False отключает проверку подписи,
    поэтому сервер доверяет любому токену, включая поддельный
    с алгоритмом «none» или с подписью, вычисленной публичным ключом
    в качестве HMAC-секрета.

    Возвращает: JSON {"valid": true, "claims": {...}}.
    """
    token = request.json.get('token')
    claims = jwt.decode(token, options={"verify_signature": False})
    return jsonify({'valid': True, 'claims': claims})


@app.route('/admin', methods=['POST'])
def admin():
    """
    Защищённый маршрут административной панели.

    Принимает токен, декодирует без проверки подписи,
    проверяет наличие роли admin.

    Возвращает: JSON {"welcome": ..., "user": ..., "role": ...}
    при role=admin, иначе JSON с error и HTTP 401/403.
    """
    token = request.json.get('token')
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        return jsonify({'error': str(e)}), 401

    if claims.get('role') != 'admin':
        return jsonify({'error': 'forbidden'}), 403

    return jsonify({
        'welcome': 'admin panel',
        'user': claims.get('sub'),
        'role': claims.get('role'),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)