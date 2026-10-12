from flask import Flask, request, redirect
import requests

app = Flask(__name__)

AUTH = 'http://auth-server:8080'
CLIENT_ID = 'test-client'
CLIENT_SECRET = 'test-secret'
REDIRECT_URI = 'http://localhost:8084/callback'


@app.route('/')
def index():
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
    app.run(host='0.0.0.0', port=8084)
