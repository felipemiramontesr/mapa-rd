import os
import json
import uuid
import hashlib
import unicodedata
from datetime import datetime
from pdf_converter import PdfConverter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLIENTS_DIR = os.path.join(BASE_DIR, 'clients')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

PROVIDER_CONFIG_PATH = os.path.join(CONFIG_DIR, 'provider_profile.json')
LEGAL_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'legal_onboarding_template.md')

class OnboardingManager:
    def __init__(self):
        self.pdf_converter = PdfConverter()
        with open(LEGAL_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            self.legal_template = f.read()
        
        with open(PROVIDER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.provider_config = json.load(f)

    def _get_next_numeric_id(self):
        tracking_file = os.path.join(DATA_DIR, 'tracking', 'client_ids.json')
        ids = {"last_id": 0}
        if os.path.exists(tracking_file):
            with open(tracking_file, 'r') as f:
                ids = json.load(f)
        
        new_id = ids.get("last_id", 0) + 1
        ids["last_id"] = new_id
        
        os.makedirs(os.path.dirname(tracking_file), exist_ok=True)
        with open(tracking_file, 'w') as f:
            json.dump(ids, f, indent=4)
            
        return f"{new_id:06d}"

    def sanitize_utf8(self, text):
        if not text: return ""
        # 1. Normalize Unicode (NFKC)
        import unicodedata
        text = str(text)
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Map potentially problematic chars to LaTeX/UTF-8 safe versions
        # Even if Pandoc handles it, we want to be safe.
        replacements = {
            "\u2013": "-", "\u2014": "-", "\u2011": "-", 
            "\u200b": "", "\ufeff": "", "\u2060": "",    
            "\u00a0": " ", "\u00ad": "", # soft hyphen
            "": "", # common corrupt char
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # 3. Strip Control Characters (except newline/tab)
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in ["\n", "\t", "\r"])
        
        return text

    def _validate_onboarding(self, client_data):
        missing = []
        
        # 0. Basic Identity
        if not client_data.get('name'): missing.append("Nombre del Cliente")
        if not client_data.get('rfc'): missing.append("RFC del Cliente")
        
        # 1. Persona Moral check
        if client_data.get('type') == 'Moral' and not client_data.get('representative_name'):
            missing.append("Nombre del Representante (Persona Moral)")
            
        # 2. Anexo A content minimum
        has_assets = any([
            client_data.get('emails'), client_data.get('domains'),
            client_data.get('phones'), client_data.get('usernames')
        ])
        if not has_assets: missing.append("Anexo A: Al menos un activo autorizado")
        if not client_data.get('acepta_activos_anexo_a'): missing.append("Anexo A: Casilla de confirmación de activos")
        
        # 3. Checkboxes obligatorios Section 2
        if not client_data.get('acepta_declaraciones'): missing.append("Sec 2: Aceptación de Declaraciones")
        if not client_data.get('acepta_terminos_servicio'): missing.append("Sec 2: Aceptación de Términos")
        if not client_data.get('acepta_aviso_privacidad'): missing.append("Anexo C: Aceptación de Aviso de Privacidad")
        
        # 4. Comercial/Technical minimum (Anexo B & F)
        commercial_fields = ['plan', 'precio', 'moneda', 'periodicidad', 'forma_pago']
        for f in commercial_fields:
            if not client_data.get(f): missing.append(f"Anexo F: Dato comercial '{f}'")
                
        return missing

    def process_new_client(self, client_data):
        # 1. Identity and Validation
        numeric_id = self._get_next_numeric_id()
        full_name = self.sanitize_utf8(client_data.get('name'))
        
        # Safe ASCII slug
        slug = unicodedata.normalize('NFKD', full_name).encode('ascii', 'ignore').decode('ascii')
        client_id_slug = slug.lower().replace(" ", "-")
        
        missing_fields = self._validate_onboarding(client_data)
        is_firmable = len(missing_fields) == 0
        
        doc_uuid = str(uuid.uuid4())
        doc_version = client_data.get('doc_version', 'v1.0')
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        fecha_str = now.strftime("%d/%m/%Y")
        
        client_dir_name = f"C-{numeric_id}__{full_name}"
        client_path = os.path.join(CLIENTS_DIR, client_dir_name)
        os.makedirs(client_path, exist_ok=True)

        # 2. Anexo Data Builders
        # Anexo A Rows
        anexo_a_rows = ""
        for e in client_data.get('emails', []): 
            anexo_a_rows += f"| Email | {e} | Propio | Sí | Principal |\n"
        for d in client_data.get('domains', []): 
            anexo_a_rows += f"| Dominio | {d} | Propio | Sí | Web corporativa |\n"
        for p in client_data.get('phones', []): 
            anexo_a_rows += f"| Teléfono | {p} | Propio | Sí | WhatsApp soporte |\n"
        for u in client_data.get('usernames', []): 
            anexo_a_rows += f"| Handle | {u} | Propio | Sí | RRSS |\n"

        if not anexo_a_rows: anexo_a_rows = "| - | - | - | - | - |\n"

        rep_section = ""
        if client_data.get('type') == 'Moral':
            rep_section = f"**Representante:** {client_data.get('representative_name')}, **Cargo:** {client_data.get('representative_role')}, **ID:** {client_data.get('representative_id_type')} {client_data.get('representative_id_num')}"

        # Test mode warning
        test_warning = ""
        if client_data.get('rfc') == self.provider_config['provider']['rfc']:
            test_warning = "::: execsummary\n### NOTA DE SISTEMA: DOCUMENTO DE AUTOCONTRATO / PRUEBA\nRFC de Cliente coincide con RFC de Proveedor. Modo Sandbox activo.\n:::\n\n"

        # 3. Filling the template with Sanitize + Variables
        md_content = self.legal_template.format(
            doc_id=numeric_id,
            doc_version=doc_version,
            fecha_emision=fecha_str,
            hora_emision=now.strftime("%H:%M:%S"),
            doc_uuid=doc_uuid,
            classification="ORDEN DE SERVICIO (VÁLIDO PARA FIRMA)" if is_firmable else "BORRADOR (NO VÁLIDO PARA FIRMA)",
            sha256_full="{sha256_full}", # Placeholder for second pass
            cliente_nombre_razon=full_name,
            cliente_tipo_persona=client_data.get('type', 'Física'),
            cliente_rfc=client_data.get('rfc', 'N/A'),
            cliente_domicilio=self.sanitize_utf8(client_data.get('address', 'N/A')),
            cliente_correo_notificaciones=client_data.get('email', 'N/A'),
            cliente_telefono_notificaciones=client_data.get('phone', 'N/A'),
            representante_section=rep_section,
            provider_name=self.provider_config['provider']['name'],
            provider_rfc=self.provider_config['provider']['rfc'],
            provider_address=self.provider_config['provider']['fiscal_address'],
            provider_arco_email=self.provider_config['provider']['arco_email'],
            privacy_notice_url=self.provider_config['provider']['privacy_notice_url'],
            check_declaraciones='X' if client_data.get('acepta_declaraciones') else ' ',
            check_terminos='X' if client_data.get('acepta_terminos_servicio') else ' ',
            check_privacidad='X' if client_data.get('acepta_aviso_privacidad') else ' ',
            check_secundarias='X' if client_data.get('acepta_finalidades_secundarias') else ' ',
            aviso_version=self.provider_config['defaults']['privacy_notice_version'],
            modalidad_servicio=client_data.get('modalidad', 'OSINT Externo'),
            frecuencia=client_data.get('frequency', 'Mensual'),
            alcance=client_data.get('alcance', 'Identidad Digital y Activos Públicos'),
            nivel_detalle=client_data.get('detail_level', 'Ejecutivo'),
            ventana_entrega_dias_habiles=client_data.get('ventana_entrega', 5),
            canal_soporte=client_data.get('canal_soporte', 'Email / WhatsApp'),
            contacto_operativo_cliente=self.sanitize_utf8(client_data.get('contacto_operativo', full_name)),
            canal_acordado=client_data.get('canal_acordado', 'WhatsApp'),
            sla_incidente_alta=self.provider_config['defaults']['sla_incident_high'],
            sla_incidente_media=self.provider_config['defaults']['sla_incident_medium'],
            retention_days=self.provider_config['defaults']['retention_days'],
            confidentiality_months=self.provider_config['defaults']['confidentiality_months'],
            plan=client_data.get('plan', 'Estándar'),
            precio=client_data.get('precio', '0.00'),
            moneda=client_data.get('moneda', 'MXN'),
            periodicidad_pago=client_data.get('periodicidad', 'Suscripción Mensual'),
            forma_pago=client_data.get('forma_pago', 'Transferencia / SPEI'),
            impuestos=client_data.get('impuestos', 'IVA no aplicable (RESICO)'),
            dias_gracia=client_data.get('dias_gracia', 5),
            aviso_terminacion_dias=client_data.get('aviso_terminacion', 30),
            fecha_inicio=fecha_str,
            renovacion_cancelacion="Renovación automática mensual. Cancelable con el preaviso pactado.",
            jurisdiction_state=client_data.get('jurisdiccion_estado', self.provider_config['defaults']['jurisdiction_state']),
            jurisdiction_city=client_data.get('jurisdiccion_ciudad', self.provider_config['defaults']['jurisdiction_city']),
            firma_cliente_nombre=self.sanitize_utf8(client_data.get('representative_name', full_name)),
            firma_cliente_cargo=client_data.get('representative_role', 'Titular'),
            firma_cliente_fecha=fecha_str,
            firma_proveedor_fecha=fecha_str,
            anexo_a_rows=anexo_a_rows,
            subencargados="Ninguno (Hospedaje propio y servicios bajo control directo)",
            breach_notify_hours=24,
            provider_tax_regime=self.provider_config['provider']['tax_regime']
        )

        md_content = self.sanitize_utf8(md_content)

        # Apply Draft logic
        if not is_firmable:
            warning_text = "\n\n::: execsummary\n### DOCUMENTO NO VÁLIDO PARA FIRMA\n**FALTANTES:** " + ", ".join(missing_fields) + "\n:::\n\n"
            md_content = "# [BORRADOR] MAPA-RD\n" + warning_text + md_content
        elif test_warning:
            md_content = test_warning + md_content

        # 4. Final metadata for LaTeX
        sha_full = hashlib.sha256(md_content.encode('utf-8')).hexdigest()
        sha_short = sha_full[:12]
        
        # Replace the full sha placeholder in the final section
        md_content = md_content.replace("{sha256_full}", sha_full)

        frontmatter = "---\n"
        frontmatter += f'title: "ORDEN DE SERVICIO Y ONBOARDING"\n'
        frontmatter += f'client_name: "{full_name}"\n'
        frontmatter += f'scan_id: "{numeric_id}"\n'
        frontmatter += f'date: "{fecha_str}"\n'
        frontmatter += f'id_label: "ID de Documento"\n'
        frontmatter += f'date_label: "Fecha de Emisión"\n'
        frontmatter += f'doc_version: "{doc_version}"\n'
        frontmatter += f'doc_uuid: "{doc_uuid}"\n'
        frontmatter += f'sha256_short: "{sha_short}"\n'
        frontmatter += f'timestamp: "{timestamp}"\n'
        frontmatter += f'classification: "{ "ORDEN DE SERVICIO" if is_firmable else "BORRADOR NO VÁLIDO" }"\n'
        frontmatter += "---\n\n"

        pdf_filename = f"C-{numeric_id}__Onboarding - {full_name}"
        md_temp_path = os.path.join(client_path, f"{pdf_filename}.md")
        
        with open(md_temp_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + md_content)

        success, pdf_path, error = self.pdf_converter.convert_to_pdf(md_temp_path)
        
        if success:
            print(f"[+] Legal Onboarding PDF created: {pdf_path}")
            if os.path.exists(md_temp_path): os.remove(md_temp_path)
        else:
            print(f"[!] Legal Onboarding PDF failed: {error}")

        # 5. Intake JSON
        intake_obj = {
            "client_id": client_id_slug,
            "client_info": {
                "numeric_id": numeric_id,
                "name": full_name,
                "type": client_data.get('type', 'Física'),
                "country": client_data.get('country', 'México'),
                "email": client_data.get('email', ''),
                "rfc": client_data.get('rfc', 'N/A'),
                "address": client_data.get('address', 'N/A')
            },
            "identity": {
                "names": [full_name],
                "emails": client_data.get('emails', []),
                "domains": client_data.get('domains', []),
                "phones": client_data.get('phones', []),
                "usernames": client_data.get('usernames', [])
            },
            "report_settings": {
                "frequency": client_data.get('frequency', 'Mensual'),
                "detail_level": client_data.get('detail_level', 'Ejecutivo'),
                "personal_data_analysis": client_data.get('personal_data_analysis', True),
                "arco_recommendations": client_data.get('arco_recommendations', True)
            }
        }
        
        intake_path = os.path.join(DATA_DIR, 'intake', f"{client_id_slug}.json")
        with open(intake_path, 'w', encoding='utf-8') as f:
            json.dump(intake_obj, f, indent=4, ensure_ascii=False)
            
        return numeric_id, full_name

if __name__ == "__main__":
    pass
