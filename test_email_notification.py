from src.notifier import Notifier
import os

def test_email():
    # Create a dummy test file
    test_file = "test_attachment.txt"
    with open(test_file, "w") as f:
        f.write("Este es un archivo de prueba para validar el sistema de notificaciones de MAPA-RD.")

    client_name = "Felipe de Jesús Miramontes Romero"
    recipients = ["info@felipemiramontesr.net", "felipemiramontesr@gmail.com"]
    
    print("[*] Iniciando prueba de envío de correo...")
    notifier = Notifier()
    scan_id = "2026-01-03__baseline__R-20260103-999"
    success = notifier.send_report(recipients, test_file, client_name, scan_id=scan_id)
    
    if success:
        print("[+] PRUEBA EXITOSA: El correo ha sido enviado.")
    else:
        print("[!] ERROR EN LA PRUEBA: No se pudo enviar el correo.")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_email()
