import os
import json
from state_manager import StateManager

class ClientManager:
    """Manages client lifecycle and onboarding workflows.
    
    This module handles the initial registration of clients, including directory
    setup, intake generation, and onboarding document creation.
    """

    def __init__(self) -> None:
        """Initialize with a StateManager instance."""
        self.state_manager = StateManager()

    def create_client_from_request(self, client_name: str, email: str) -> str:
        """Handle the initial client capture flow (Flow 5.1).
        
        Args:
            client_name: Full name of the client.
            email: Primary contact email.
            
        Returns:
            The unique client_id.
        """
        client_id = self.state_manager._get_or_create_client_id(client_name)
        self.state_manager.update_client(client_id, name=client_name, email=email, intake_status="GENERADO")
        
        # Save DATOS_CLIENTE file
        # Naming: MAPA-RD - DATOS_CLIENTE - IDCLIENTE - NOMBRE - IDREPORTE - FECHA
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        safe_name = self.state_manager.sanitize_filename(client_name)
        datos_filename = f"MAPA-RD - DATOS_CLIENTE - {client_id} - {safe_name} - C-0001 - {date_str}.json"
        datos_path = os.path.join(self.state_manager.TRACKING_DIR, datos_filename)
        
        datos = {
            "client_id": client_id,
            "name": client_name,
            "email": email,
            "created_at": now.isoformat()
        }
        
        with open(datos_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
            
        print(f"[+] DATOS_CLIENTE generated: {datos_filename}")
        return client_id

    def generate_onboarding(self, client_id: str) -> bool:
        """Generate the Welcome Kit/Onboarding PDF (Flow 5.2).
        
        Args:
            client_id: The ID of the client.
            
        Returns:
            True if generation initiated successfully.
        """
        client = self.state_manager.get_client(client_id)
        if not client: return False
        
        # Logic to generate ONBOARDING PDF would go here
        # For now, we update status and simulate the file creation
        print(f"[*] Generating ONBOARDING for {client['name']}...")
        return True

    def generate_intake_base(self, client_id: str, identity_data: dict) -> bool:
        """Create the initial Intake JSON baseline (Flow 5.3).
        
        Args:
            client_id: The ID of the client.
            identity_data: Dictionary of known identity assets (emails, domains).
            
        Returns:
            True if intake created successfully.
        """
        client = self.state_manager.get_client(client_id)
        if not client: return False
        
        # Identity data includes emails, phones, etc.
        # This is a baseline setup
        intake_data = {
            "client_info": client,
            "identity": identity_data,
            "report_type": "baseline",
            "status": "GENERADO"
        }
        
        # Save INTAKE file
        intake_path = os.path.join(os.path.dirname(self.state_manager.TRACKING_DIR), 'intake', f"{client_id}.json")
        os.makedirs(os.path.dirname(intake_path), exist_ok=True)
        
        with open(intake_path, 'w', encoding='utf-8') as f:
            json.dump(intake_data, f, indent=4, ensure_ascii=False)
            
        print(f"[+] INTAKE_BASE generated for {client_id}")
        return True
