import smtplib
import json
import os
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders, utils
from email.header import Header

class Notifier:
    def __init__(self, config_path="03_Config/config.json", config_dict=None):
        # 1. Configuration Loading (Env Vars > Config Dict > Config File)
        self.config = {}
        
        # Load from file first (if exists) as fallback base
        if os.path.exists(config_path):
             try:
                 with open(config_path, 'r') as f:
                     self.config = json.load(f).get('email', {})
             except: pass
        
        # Override with passed dict
        if config_dict:
            self.config.update(config_dict)
            
        # Override with Env Vars (Standard Keys)
        env_map = {
            "EMAIL_BACKEND": "backend",
            "SMTP_HOST": "smtp_host",
            "SMTP_PORT": "smtp_port",
            "SMTP_USER": "smtp_user",
            "SMTP_PASS": "smtp_pass",
            "SMTP_TLS": "smtp_tls",
            "SMTP_FROM": "sender_email",
            "EMAIL_TO_OVERRIDE": "to_override"
        }
        for env_key, conf_key in env_map.items():
            if os.getenv(env_key):
                self.config[conf_key] = os.getenv(env_key)
        
        # 2. Key Settings & Validation
        self.backend = self.config.get("backend", "stub").lower()
        self.sender = self.config.get("sender_email", "noreply@mapa-rd.com")
        self.override_to = self.config.get("to_override")
        
        self.outbox_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data', 'outbox')
        
        if self.backend == "stub":
            if not os.path.exists(self.outbox_dir):
                os.makedirs(self.outbox_dir, exist_ok=True)
        elif self.backend == "smtp":
            # Strict Validation for SMTP
            required = ["smtp_host", "smtp_port", "smtp_user", "smtp_pass"]
            missing = [k for k in required if not self.config.get(k)]
            if missing:
                raise ValueError(f"SMTP Backend selected but missing config: {missing}")

    def send_report(self, receiver_emails, report_path, client_name, scan_id=None, subject=None, body=None):
        start_time = time.time()
        
        # routing safety
        final_to = receiver_emails
        if self.override_to:
            print(f"[LOG] EMAIL_ROUTING | override=active | to_effective={self.override_to} | to_original={receiver_emails}")
            final_to = [self.override_to]

        # Extract report number logic (same as before)
        formatted_number = "000"
        if scan_id and "R-" in scan_id:
            try:
                formatted_number = scan_id.split("-")[-1]
            except: pass
        else:
             # Fallback
             pass

        msg = MIMEMultipart()
        msg['From'] = f"MAPA-RD <{self.sender}>"
        msg['To'] = ", ".join(final_to)
        msg['Reply-To'] = self.sender
        msg['Subject'] = subject if subject else f"Reporte MAPA-RD #{formatted_number} | {client_name}"
        msg['Date'] = utils.formatdate(localtime=True)
        
        # Improve Deliverability: Use sender domain in Message-ID
        domain_suffix = self.sender.split("@")[-1] if "@" in self.sender else None
        msg['Message-ID'] = utils.make_msgid(domain=domain_suffix)

        print(f"[LOG] EMAIL_PREPARED | report_id={scan_id} | backend={self.backend} | to={msg['To']} | subject={msg['Subject']}")

        body_text = body if body else (
            f"Buen día,\n\n"
            f"Se adjunta el Reporte de Inteligencia OSINT correspondiente al análisis realizado para {client_name}.\n\n"
            f"El documento presenta una evaluación estructurada de la huella digital identificada en fuentes abiertas.\n\n"
            f"Atentamente,\n"
            f"MAPA-RD\n"
        )
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

        # Attachment
        if report_path:
            if os.path.exists(report_path):
                with open(report_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(report_path)}")
                    msg.attach(part)
            else:
                print(f"[LOG] EMAIL_SEND_FAIL | report_id={scan_id} | backend={self.backend} | error_class=FileNotFound | error_message=Attachment missing")
                return False, "Attachment missing"

        # Dispatch
        try:
            print(f"[LOG] EMAIL_SEND_ATTEMPT | report_id={scan_id} | backend={self.backend} | host={self.config.get('smtp_host', 'N/A')}")
            
            if self.backend == "stub":
                result_id = self._send_stub(msg, client_name, scan_id)
            else:
                result_id = self._send_smtp(msg, scan_id)
            
            duration = int((time.time() - start_time) * 1000)
            print(f"[LOG] EMAIL_SEND_SUCCESS | report_id={scan_id} | backend={self.backend} | message_id={result_id} | duration_ms={duration}")
            return True, result_id

        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            print(f"[LOG] EMAIL_SEND_FAIL | report_id={scan_id} | backend={self.backend} | error_class={type(e).__name__} | error_message={str(e)[:200]} | duration_ms={duration}")
            return False, str(e)

    def _send_stub(self, msg, client_name, scan_id):
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{scan_id}.json"
        filepath = os.path.join(self.outbox_dir, filename)
        data = {
            "to": msg['To'],
            "subject": msg['Subject'],
            "message_id": msg['Message-ID'],
            "client": client_name
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return msg['Message-ID'] or "stub-id"

    def _send_smtp(self, msg, scan_id=None):
        host = self.config['smtp_host']
        port = int(self.config['smtp_port'])
        user = self.config['smtp_user']
        password = self.config['smtp_pass']
        use_tls = str(self.config.get('smtp_tls', 'true')).lower() == 'true'

        max_retries = 3
        last_error = None
        
        for attempt in range(1, max_retries + 1):
            try:
                if port == 465:
                    server = smtplib.SMTP_SSL(host, port, timeout=30)
                else:
                    server = smtplib.SMTP(host, port, timeout=30)
                    if use_tls:
                        server.starttls()
                
                if user and password:
                    server.login(user, password)
                
                server.send_message(msg)
                server.quit()
                return msg['Message-ID']
            except Exception as e:
                last_error = e
                backoff = 2 ** attempt
                if attempt < max_retries:
                    print(f"[LOG] EMAIL_SEND_RETRY | attempt={attempt} | backoff={backoff}s | error={str(e)[:100]}")
                    time.sleep(backoff)
                else:
                    print(f"[ALERT] EMAIL_SEND_FAIL_FINAL | report_id={scan_id} | email_to={msg['To']} | error_class={type(last_error).__name__} | error_message={str(last_error)[:200]} | timestamp={datetime.now().isoformat()}")
                    raise last_error
