import sys
import os
import json
import shutil
from datetime import datetime

# Add Src to path
sys.path.append(os.path.join(os.getcwd(), '07_Src'))

from report_generator import ReportGenerator
from notifier import Notifier

def run_injection_test():
    print("[*] Starting Data Injection Pipeline for Ana Flores (Aggressive)...")
    
    # Configuration
    client_name = "Ana Flores (v1.0 Mock)"
    client_id = "R-ANA-FLORES-MOCK-001"
    target_email = "anafbaca@gmail.com"
    mock_data_path = os.path.join("04_Data", "hibp_mock_anafbaca.json")
    
    # Determine base directory
    base_dir = os.path.join("04_Data", "raw", client_id)
    os.makedirs(base_dir, exist_ok=True)
    
    # Load HIBP Data
    if not os.path.exists(mock_data_path):
        print("[-] Mock data file not found.")
        return

    with open(mock_data_path, 'r', encoding='utf-8') as f:
        hibp_data = json.load(f)
        
    print(f"[*] Loaded {len(hibp_data)} breaches from mock file.")
    
    # Transform HIBP data into Flat Findings List expected by ReportGenerator
    findings = []
    
    # 1. Breaches
    for breach in hibp_data:
        # Determine risk
        is_password = "Contraseñas" in breach.get("DataClasses", [])
        risk = "P0" if is_password else "P1"
        
        finding = {
            "module": "sfp_haveibeenpwned",
            "type": "BIO_Public_Exposure", 
            "data": f"Breach: {breach['Name']}",
            "description": f"Exposed in {breach['Title']} ({breach['BreachDate']}). Data: {', '.join(breach['DataClasses'])}",
            "risk_score": risk,
            "validation_status": "VULNERABLE",
            # Keys required by _generate_threat_narrative
            "category": "Fuga de Datos",
            "entity": "Credenciales Comprometidas" if is_password else "Datos Personales",
            "source_name": "sfp_citadel", # Maps to 'Bases de Datos de Filtraciones'
            # Enhanced Data for Report V83
            "breach_title": breach.get("Title", breach.get("Name")),
            "breach_desc": breach.get("Description"),
            "breach_classes": breach.get("DataClasses", []),
            "breach_date": breach.get("BreachDate")
        }
        findings.append(finding)
    
    # 2. Mock Email Finding
    findings.append({
        "module": "sfp_google",
        "type": "EMAIL_ADDR",
        "data": target_email,
        "description": "Correo electrónico confirmado.",
        "risk_score": "P3",
        "validation_status": "CONFIRMED",
        "category": "Contacto",
        "entity": "Email",
        "source_name": "sfp_googlesearch"
    })
    
    print("[*] Generating Report...")
    generator = ReportGenerator()
    
    # Force Mock Client Registration
    print(f"[*] Registering Mock Client: {client_id}")
    generator.state_manager.create_client(client_id, client_name, "PF")
    
    # generate_report returns a dist with paths
    result = generator.generate_report(client_id, "I-MOCK-001", client_id, findings)
    pdf_path = result.get("pdf_path")
    
    if pdf_path and os.path.exists(pdf_path):
        print(f"[+] Report Generated Successfully: {pdf_path}")
        
        # [SILENCED V31] Disabled automatic email notification
        # print("[*] Sending Email Notification...")
        # override_config = {"backend": "smtp"}
        # notifier = Notifier(config_dict=override_config)
        
        # success, msg = notifier.send_report(
        #     receiver_emails=["felipemiramontesr@gmail.com", "anafbaca@gmail.com"],
        #     report_path=pdf_path,
        #     client_name=client_name,
        #     scan_id=client_id,
        #     subject=f"ALERTA DE SEGURIDAD CRÍTICA: Reporte Ana Flores (vFinal)"
        # )
        
        # if success:
        #     print("[+] Email Sent!")
        # else:
        #     print(f"[-] Email Failed: {msg}")
        pass
            
    else:
        print("[-] Report Generation Failed.")

if __name__ == "__main__":
    run_injection_test()
