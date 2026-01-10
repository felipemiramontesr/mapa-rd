import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr

# Config Hardcoded for Verify (We will read from file in production, but here we want to be explicit)
# Please check these values match what you expect
SMTP_HOST = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = "info@felipemiramontesr.net"
SMTP_PASS = "Fm666.%%1096461"
SENDER_EMAIL = "info@felipemiramontesr.net"
SENDER_NAME = "MAPA-RD Debug"

RECIPIENT = "info@felipemiramontesr.net"

def send_simple():
    print(f"[*] Connecting to {SMTP_HOST}:{SMTP_PORT}...")
    
    msg = MIMEText("Prueba de depuración interna. ¿Llega este correo a la misma cuenta que lo envía?", "plain", "utf-8")
    msg['Subject'] = "DEBUG: Auto-envío Hostinger"
    msg['From'] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg['To'] = RECIPIENT
    
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
            server.set_debuglevel(1) # Enable verbose SMTP logging
            print("[*] Logging in...")
            server.login(SMTP_USER, SMTP_PASS)
            print("[*] Sending...")
            server.send_message(msg)
            print("[+] Email SENT Successfully via SMTP_SSL.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    send_simple()
