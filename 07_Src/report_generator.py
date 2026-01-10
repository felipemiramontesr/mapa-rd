import os
import json
import unicodedata
from datetime import datetime
from pdf_converter import PdfConverter
from state_manager import StateManager
from qc_module import QCModule

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '08_Templates', 'cliente_final.md')
RECLAMACION_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '08_Templates', 'reclamacion.md')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '04_Data')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports')
ARCO_ROOT = os.path.join(DATA_DIR, 'arco')
TRACKING_DIR = os.path.join(DATA_DIR, 'tracking')

class ReportGenerator:
    def __init__(self, state_manager=None):
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            self.template = f.read()
        with open(RECLAMACION_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            self.reclamacion_template = f.read()
        self.pdf_converter = PdfConverter()
        # Dependency Injection: Use provided state_manager or new instance
        self.state_manager = state_manager if state_manager else StateManager()
        self.REPORTS_DIR = REPORTS_DIR
        self.ARCO_ROOT = ARCO_ROOT
        self.QCModule = QCModule
        self.ensure_dirs()

    def ensure_dirs(self):
        for d in [self.REPORTS_DIR, self.ARCO_ROOT, self.state_manager.TRACKING_DIR]:
            if not os.path.exists(d):
                os.makedirs(d)

    def _get_or_create_client_id(self, client_name):
        id_file = os.path.join(TRACKING_DIR, 'client_ids.json')
        if not os.path.exists(id_file):
            data = {"last_id": 0, "clients": {}}
        else:
            with open(id_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Normalize name for lookup
        norm_name = self.sanitize_filename(client_name).lower()
        if norm_name in data.get("clients", {}):
            return data["clients"][norm_name]
        
        # Create new ID
        new_id = data.get("last_id", 0) + 1
        data["last_id"] = new_id
        if "clients" not in data: data["clients"] = {}
        data["clients"][norm_name] = f"{new_id:07d}"
        
        with open(id_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        return f"{new_id:07d}"

    def sanitize_filename(self, name):
        return name.replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n").replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N")

    def sanitize_text(self, text):
        if not text: return ""
        # 1. Normalize Unicode (NFKC) to fix compatibility characters
        import unicodedata
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Explicit character replacements
        replacements = {
            "\u2013": "-", "\u2014": "-", "\u2011": "-", # Dashes
            "\u200b": "", "\ufeff": "", "\u2060": "",    # Zero width / BOM
            "\u00a0": " "                                # Non-breaking space
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # 3. Strip Control Characters (0x00-0x1F except newline/tab)
        text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in ["\n", "\t"])
        
        return text

    def generate_report(self, client_id, intake_id, report_id, findings, report_type="BASELINE"):
        # 1. Validation and Metadata
        client = self.state_manager.get_client(client_id)
        if not client: raise ValueError(f"Client {client_id} not found.")

        report_type = report_type.upper()
        if report_type not in self.state_manager.REPORT_TYPES:
            raise ValueError(f"Tipo de reporte invalido: {report_type}")

        now = datetime.now()
        report_date_str = now.strftime("%Y-%m-%d")
        
        # 2. Build nomenclature metadata
        client_name = client["client_name_full"]
        client_slug = client["client_name_slug"]
        
        # BASE nomenclature: MAPA-RD - TIPO_ARCHIVO - IDCLIENTE - NOMBRE_COMPLETO_CLIENTE - IDREPORTE - FECHA
        def build_name(tipo_archivo):
            return f"MAPA-RD - {tipo_archivo} - {client_id} - {client_slug} - {report_id} - {report_date_str}"

        base_report_name = build_name("REPORTE")
        
        # 4. Prepare Sections
        months_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        nice_date = f"{now.day} de {months_es[now.month]} de {now.year}"
        
        is_rescue = (report_type == "RESCUE")
        exec_summary = self.sanitize_text(self._generate_executive_summary(findings, is_rescue))
        threat_narrative = self.sanitize_text(self._generate_threat_narrative(findings))
        action_plan = self.sanitize_text(self._generate_action_plan(findings))
        
        # ARCO Logic
        arco_data = self._classify_arco_findings(findings)
        arco_expl = self.sanitize_text(self._generate_arco_explanation())
        arco_cases = self.sanitize_text(self._generate_arco_cases(arco_data))
        
        telecom_section = self.sanitize_text(self._generate_telecom_section(findings))
        conclusion = self.sanitize_text(self._generate_conclusion(findings))
        
        # Generate individual ARCO files
        arco_annexes_content = self._generate_arco_documents(client_name, client_id, report_id, report_date_str, arco_data)

        # Reclamación Section
        reclamacion_content = self.reclamacion_template.format(
            client_name=client_name,
            scan_id=report_id,
            date=nice_date
        )

        # Define Types and Scopes
        # Define Types and Scopes
        type_map = {
            "BASELINE": ("Diagnóstico Inicial (Baseline)", "Análisis exhaustivo de todas las fuentes públicas para establecer su estado de seguridad."),
            "FREQUENCY": ("Monitoreo Periódico (Frequency)", "Seguimiento de hallazgos detectados en el último diagnóstico para verificar su cierre o persistencia."),
            "INCIDENT": ("Análisis de Incidente", "Estudio focalizado sobre un evento anómalo de exposición reportado recientemente."),
            "RESCUE": ("Diagnóstico de Rescate", "Reconstrucción oficial de un diagnóstico previo para recuperar el estado de seguridad.")
        }
        
        type_name, scope_desc = type_map.get(report_type, ("Análisis Especial", "Evaluación de seguridad digital personalizada."))
        if is_rescue:
            type_name += " (Modo Rescate)"

        # 5. Fill Template
        body_content = self.template.format(
            client_name=client_name,
            client_id_field=client_id,
            scan_id=report_id,
            date=nice_date,
            report_type_description=type_name,
            report_scope_description=scope_desc,
            executive_summary_content=exec_summary,
            threat_narrative_section=threat_narrative,
            action_plan_section=action_plan,
            arco_explanation=arco_expl,
            arco_cases=arco_cases,
            telecom_section=telecom_section,
            conclusion_section=conclusion,
            arco_formats=arco_annexes_content,
            technical_annex_summary=f"Se detectaron un total de {len(findings)} registros brutos analizados."
        )
        
        # Add Reclamación at the very end as Section 9 (Implicitly after Section 8)
        body_content += f"\n\n***\n\n## 9. Formato de Reclamación (SIEMPRE)\n{reclamacion_content}"

        # 6. Save Files
        md_filepath = os.path.join(self.REPORTS_DIR, f"{base_report_name}.md")
        
        frontmatter = "---\n"
        frontmatter += f'title: "MAPA-RD - REPORTE DE INTELIGENCIA"\n'
        frontmatter += f'client_name: "{client_name}"\n'
        frontmatter += f'report_id: "{report_id}"\n'
        frontmatter += f'report_date: "{nice_date}"\n'
        frontmatter += "---\n\n"
        
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + body_content)
            
        # Technical Data Nomenclature (Spec 6)
        json_base_name = build_name("METADATA")
        json_filepath = os.path.join(self.REPORTS_DIR, f"{json_base_name}.json")
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=2, ensure_ascii=False)
 
        # 7. PDF Generation
        self.pdf_converter.template_name = "report_intel.tex"
        final_pdf_path = self._generate_pdf_version(client_name, report_id, frontmatter, body_content, md_filepath, base_report_name)
        
        return {
            "report_id": report_id,
            "base_name": base_report_name,
            "md_path": md_filepath,
            "pdf_path": final_pdf_path,
            "json_path": json_filepath,
            "arco_dir": os.path.join(self.ARCO_ROOT, build_name("ARCO")) if arco_data else None
        }


        return md_filepath

    def _classify_arco_findings(self, findings):
        # Returns dict: { (provider, right): [findings] }
        classified = {}
        
        source_map = {
            "sfp_citadel": "Bases de Datos de Filtraciones",
            "sfp_intfiles": "Servidores de Archivos Públicos",
            "sfp_accounts": "Redes Sociales y Foros",
            "sfp_googlesearch": "Google",
            "sfp_bingsearch": "Bing",
            "sfp_filemeta": "Repositorios de Documentos",
            "sfp_dnsresolve": "Registros de Internet"
        }

        for f in findings:
            category = f.get('category', 'Other')
            source_raw = f.get('source_name', 'Terceros')
            if source_raw in ['Internal', 'SpiderFoot UI']: continue
            
            provider = source_map.get(source_raw, "Proveedor Externo")
            
            # Simplified classification logic
            right = "NO_ARCO"
            if category in ['Identity', 'Contact']:
                right = "CANCELACION"
            elif category == 'Social Footprint':
                right = "OPOSICION"
            elif category == 'Data Leak' and f.get('risk_score') == 'P0':
                right = "ACCESO"
            
            if right != "NO_ARCO":
                key = (provider, right)
                if key not in classified: classified[key] = []
                classified[key].append(f)
                
        return classified

    def _generate_arco_documents(self, client_name, client_id, id_reporte, report_date_str, arco_data):
        if not arco_data:
            return ""
            
        def build_name(tipo_archivo, extra=""):
            base = f"MAPA-RD - {tipo_archivo} - {client_id} - {self.sanitize_filename(client_name)} - {id_reporte} - {report_date_str}"
            if extra: base += f" - {extra}"
            return base

        base_arco_name = build_name("ARCO")
        arco_dir = os.path.join(self.ARCO_ROOT, base_arco_name)
        if not os.path.exists(arco_dir):
            os.makedirs(arco_dir)
            
        annexes_text = ""
        
        for (provider, right), findings in arco_data.items():
            safe_provider = self.sanitize_filename(provider)
            # Naming for individual ARCO: MAPA-RD - ARCO - IDCLIENTE - NOMBRE - IDREPORTE - FECHA - DERECHO - PROVEEDOR
            arco_md_name = f"{base_arco_name} - {right} - {safe_provider}.md"
            arco_path = os.path.join(arco_dir, arco_md_name)
            
            content = f"# Solicitud de Derecho de {right}\n\n"
            content += f"Yo, **{client_name}**, actuando bajo mi propio derecho, solicito formalmente el ejercicio de mi derecho de **{right}** ante **{provider}**.\n\n"
            content += "Fundamento legal: Ley Federal de Protección de Datos Personales en Posesión de los Particulares.\n\n"
            content += "Detalle de hallazgos:\n"
            for f in findings[:5]:
                content += f"- {f.get('entity', 'Dato')} detectado en {f.get('source_name')}\n"
            
            with open(arco_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.pdf_converter.convert_to_pdf(arco_path)
            os.remove(arco_path)
            
            annexes_text += f"\n### Anexo: Solicitud de {right} ({provider})\n{content}\n"

        # 2. Generate ARCO_GUIA
        guia_name = build_name("ARCO_GUIA")
        guia_path = os.path.join(arco_dir, f"{guia_name}.md")
        guia_content = "# Guía de Gestión de Derechos ARCO\n\n"
        guia_content += f"Se han generado {len(arco_data)} solicitudes individuales para su gestión.\n\n"
        guia_content += "| Proveedor | Derecho | Objetivo |\n|---|---|---|\n"
        for (provider, right) in arco_data.keys():
            guia_content += f"| {provider} | {right} | Recuperar control de información |\n"
            
        guia_content += "\n**Servicio Adicional:** MAPA-RD puede gestionar estas solicitudes por usted bajo autorización expresa."
        
        with open(guia_path, 'w', encoding='utf-8') as f:
            f.write(guia_content)
        self.pdf_converter.convert_to_pdf(guia_path)
        os.remove(guia_path)
        
        return annexes_text

    def _generate_executive_summary(self, findings, is_rescue=False):
        p0_len = len([f for f in findings if f.get('risk_score') == 'P0'])
        
        level = "CRÍTICO" if p0_len > 0 else "MEDIO"
        summary = ""
        
        if is_rescue:
            summary += "> **NOTA DE RESCATE:** Este documento es una reconstrucción oficial de un diagnóstico previo para asegurar la integridad de su información.\n\n"
            
        summary += f"**Estado General de Riesgo:** {level}\n\n"
        
        summary += "Tras un análisis exhaustivo, hemos determinado que su identidad digital presenta vulnerabilidades que requieren atención. "
        
        if p0_len > 0:
            summary += "Se detectaron filtraciones de credenciales en servicios externos, lo que genera un riesgo real de suplantación de identidad y fraude financiero si no se actúa de inmediato.\n\n"
            summary += "### Principales Hallazgos:\n"
            summary += "1. **Filtración de Accesos:** Sus claves han sido expuestas en brechas de seguridad de terceros (Urgencia: Inmediata).\n"
            summary += "2. **Exposición de Documentos:** Existen archivos con sus datos personales accesibles para descarga (Urgencia: Inmediata).\n"
            summary += "3. **Rastreo Telefónico:** Su número celular es público y vulnerable a estafas (Urgencia: Media).\n"
        else:
            summary += "No se detectaron filtraciones críticas recientes, pero su huella digital permite un rastreo personal que escala su nivel de riesgo a Medio.\n"
            
        return summary

    def _generate_threat_narrative(self, findings):
        # Human-friendly source map
        source_map = {
            "sfp_citadel": "Bases de Datos de Filtraciones",
            "sfp_intfiles": "Servidores de Archivos Públicos",
            "sfp_accounts": "Redes Sociales y Foros",
            "sfp_googlesearch": "Motor de Búsqueda (Google)",
            "sfp_bingsearch": "Motor de Búsqueda (Bing)",
            "sfp_filemeta": "Repositorios de Documentos",
            "sfp_dnsresolve": "Registros de Infraestructura",
            "Internal": "Fuentes Propias Analizadas"
        }

        # Human-friendly entity map
        entity_map = {
            "Compromised Credentials": "Claves de Acceso Filtradas",
            "Sensitive File Exposed": "Documentos Privados Expuestos",
            "Document Metadata": "Rastros en Archivos Digitales",
            "Full Name": "Nombre y Apellidos",
            "Phone": "Número Telefónico Personal",
            "Email": "Correo Electrónico Privado",
            "Handle/User": "Nombre de Usuario",
            "External Account": "Cuenta en Plataformas Externas"
        }

        # Consolidation into a few high-impact threat units
        threat_blocks = []
        
        # Case A: Credentials
        creds = [f for f in findings if f.get('risk_score') == 'P0']
        if creds:
            for f in creds[:3]: # Take unique high-value ones
                threat_blocks.append({
                    "nombre": "Fraude Financiero y Acceso Ilegal",
                    "donde": f"Plataforma: {source_map.get(f.get('source_name'), 'Filtraciones Masivas')}\nTipo: Filtración de seguridad\nEstado: Activo (Riesgo de reutilización)",
                    "que": entity_map.get(f.get('entity'), 'Información de Acceso'),
                    "riesgo_real": "Un atacante puede probar estas claves en sus cuentas actuales o servicios bancarios para sustraer fondos o información confidencial.",
                    "nivel": "ALTO",
                    "accion": "Cambio inmediato de contraseñas y activación de Verificación en 2 Pasos (2FA)."
                })

        # Case B: Identity/Files
        files = [f for f in findings if f.get('category') == 'Identity' or f.get('category') == 'Data Leak' and f.get('risk_score') != 'P0']
        if files:
            for f in files[:2]:
                threat_blocks.append({
                    "nombre": "Suplantación de Identidad",
                    "donde": f"Sitio: {source_map.get(f.get('source_name'), 'Internet Abierta')}\nTipo: Indexación pública de documentos\nEstado: Activo",
                    "que": entity_map.get(f.get('entity'), 'Datos de Identidad'),
                    "riesgo_real": "Extranjeros pueden usar sus documentos o datos para realizar trámites legales o comerciales en su nombre.",
                    "nivel": "ALTO",
                    "accion": "Solicitud de retiro (ARCO) y monitoreo de estados bancarios."
                })

        # Case C: Contact
        phones = [f for f in findings if f.get('category') == 'Contact']
        if phones:
            threat_blocks.append({
                "nombre": "Extorsión o Estafas Telefónicas",
                "donde": "Plataforma: Directorios Públicos / Foros\nTipo: Registro abierto\nEstado: Activo",
                "que": "Número telefónico y correo personal",
                "riesgo_real": "Su información personal es el insumo principal para guiones de estafa o llamadas de extorsión dirigidas (Phishing).",
                "nivel": "MEDIO",
                "accion": "Registro en listas de exclusión (REPEP) y reducción de visibilidad en redes sociales."
            })

        # Render MD blocks
        content = ""
        for i, t in enumerate(threat_blocks[:8]):
            content += f"### 2.{i+1} {t['nombre']}\n"
            content += f"**¿Dónde ocurrió?**\n{t['donde']}\n\n"
            content += f"**Información comprometida:** {t['que']}\n\n"
            content += f"**Riesgo real:** {t['riesgo_real']}\n\n"
            content += f"**Nivel de riesgo:** {t['nivel']}\n\n"
            content += f"**Qué debe hacer:** {t['accion']}\n\n***\n"
            
        return content

    def _generate_exposure_details(self, findings):
        leaks = [f for f in findings if f.get('risk_score') == 'P0']
        if not leaks:
            return "No se encontraron sus datos en filtraciones masivas recientes."
            
        content = "Hemos detectado los siguientes tipos de datos expuestos en la red:\n\n"
        content += "| Dato Expuesto | Gravedad de la Amenaza |\n|---|---|\n"
        
        # Map technical internal types to plain Spanish
        etype_map = {
            "Compromised Credentials": "Contraseñas y Accesos Filtrados",
            "Sensitive File Exposed": "Documentos Privados Expuestos",
            "Document Metadata": "Rastros en Archivos Digitales",
            "Full Name": "Identidad Completa",
            "Phone": "Número Telefónico Privado"
        }
        
        processed = set()
        for l in leaks[:15]:
            raw_etype = l.get('entity', 'Dato Personal')
            etype = etype_map.get(raw_etype, raw_etype)
            if etype in processed: continue
            content += f"| {etype} | ALTA |\n"
            processed.add(etype)
            
        return content

    def _generate_action_plan(self, findings):
        content = "| Caso Detectado | Acción Concreta | Quién Ejecuta | Tiempo | Resultado Esperado |\n"
        content += "|---|---|---|---|---|\n"
        
        if any(f.get('risk_score') == 'P0' for f in findings):
            content += "| Filtración de Claves | Cambio de contraseña + 2FA | Titular | 15 min | Evita el ingreso de extraños |\n"
        
        if any(f.get('category') == 'Identity' for f in findings):
            content += "| Datos Expuestos | Solicitud de Borrado (ARCO) | MAPA-RD | 3 días | Elimina el rastro público |\n"
            
        if any(f.get('category') == 'Contact' for f in findings):
            content += "| Teléfono Público | Registro en REPEP | Titular | 5 min | Reduce llamadas de spam/estafa |\n"
            
        content += "| Gestión de Riesgos | Monitoreo Mensual | MAPA-RD | Continuo | Alerta temprana de nuevas brechas |\n"
        
        return content

    def _generate_privacy_rights(self, findings):
        candidates = [f for f in findings if f.get('category') in ['Identity', 'Social Footprint', 'Contact']]
        
        if not candidates:
            return "En este análisis no se detectaron sitios externos que requieran un ejercicio formal de Derechos ARCO bajo su titularidad."

        content = "Usted tiene el derecho legal de exigir que su información privada sea borrada o bloqueada de sitios que no deberían tenerla:\n\n"
        
        # Map technical internal types to plain Spanish categories
        source_map = {
            "sfp_citadel": "Bases de Datos de Filtraciones",
            "sfp_intfiles": "Servidores de Archivos Públicos",
            "sfp_accounts": "Redes Sociales y Foros Externos",
            "sfp_bingsearch": "Motores de Búsqueda Públicos",
            "sfp_googlesearch": "Motores de Búsqueda Públicos",
            "sfp_filemeta": "Repositorios de Documentos",
            "sfp_dnsresolve": "Registros de Infraestructura de Internet"
        }

        seen_sources = set()
        for f in candidates:
            raw_src = f.get('source_name', 'Bases de Datos Externas')
            if raw_src == 'Internal' or raw_src == 'SpiderFoot UI': continue
            
            clean_src = source_map.get(raw_src, "Bases de Datos de Información Pública")
            if clean_src in seen_sources: continue
            
            content += f"- En **{clean_src}**: Recomendamos ejercer su derecho de **CANCELACIÓN** u **OPOSICIÓN**.\n"
            seen_sources.add(clean_src)
            if len(seen_sources) >= 3: break
        
        content += "\n**Acción:** Hemos preparado para usted los formatos de solicitud legal necesarios. Solo requieren su firma para proceder con la eliminación de estos rastros."
        return content

    def _generate_legal_disclaimer(self):
        return "Este análisis se realizó bajo un entorno controlado y ético, utilizando únicamente información que ya es pública en internet."

    def _generate_arco_explanation(self):
        return """Los derechos **ARCO** son su herramienta legal para recuperar el control de su información en internet:
1. **Acceso:** Saber quién tiene sus datos.
2. **Rectificación:** Corregir datos erróneos.
3. **Cancelación:** Solicitar que borren su información definitivamente.
4. **Oposición:** Exigir que dejen de usar sus datos para fines que usted no autorizó.

Al ejercer estos derechos, obligamos a las empresas y motores de búsqueda a retirar su información de la vista pública."""

    def _generate_arco_cases(self, arco_data):
        if not arco_data:
            return "No se detectaron casos que ameriten ARCO actualmente."
            
        content = "Hemos identificado los siguientes puntos donde aplica la intervención legal:\n\n"
        content += "| Derecho Aplicable | Proveedor | Objetivo |\n|---|---|---|\n"
        
        for (provider, right) in arco_data.keys():
            content += f"| {right} | {provider} | Recuperar control de información |\n"
            
        return content

    def _generate_telecom_section(self, findings):
        return """La exposición de su número telefónico genera riesgos críticos de **Spam**, **Fraudes vía WhatsApp** y **Extorsiones**. 

**Acciones recomendadas:**
1. **REPEP:** Inscribirse en el Registro Público para Evitar Publicidad.
2. **Privacidad Biométrica:** Nunca autorice el uso de su voz en llamadas sospechosas.
3. **Servicio MAPA-RD:** Podemos encargarnos de la gestión completa de estas solicitudes para limpiar su historial en directorios comerciales con un costo adicional."""

    def _generate_conclusion(self, findings):
        return """Actualmente su nivel de exposición es significativo debido a las filtraciones de seguridad detectadas. Al ejecutar el **Plan de Acción**, reduciremos su superficie de ataque en un 80%, protegiendo su patrimonio y su tranquilidad.

**Próximos Pasos con MAPA-RD:**
- Firmar los anexos ARCO adjuntos.
- Iniciar el monitoreo continuo para detectar nuevas filtraciones antes de que sean explotadas."""

    def _generate_arco_formats(self, client_name):
        acc = f"""### Anexo A: Formato ARCO – ACCESO
Yo, **{client_name}**, solicito el ACCESO a todos mis datos personales almacenados en sus sistemas conforme a la ley vigente."""
        can = f"""### Anexo B: Formato ARCO – CANCELACIÓN
Yo, **{client_name}**, solicito la CANCELACIÓN de mis registros y el borrado inmediato de toda información vinculada a mi identidad."""
        opo = f"""### Anexo C: Formato ARCO – OPOSICIÓN
Yo, **{client_name}**, manifiesto mi OPOSICIÓN al tratamiento de mis datos personales para fines publicitarios o de indexación pública."""
        
        return acc + "\n\n" + can + "\n\n" + opo + "\n\n### Anexo D: Guía de Envío\n1. Firme el formato correspondiente.\n2. Adjunte copia de su INE/Pasaporte.\n3. Envíe por correo electrónico al área de privacidad del sitio indicado."

    def _generate_pdf_version(self, client_name, scan_id, frontmatter, body_content, original_md_path, base_name):
        # Inject LaTeX for Printing
        body_content = body_content.replace("\n---\n", "\n***\n")
        lines = body_content.split('\n')
        
        try:
             exec_sum_index = next(i for i, line in enumerate(lines) if line.strip().startswith("## 1."))
             lines = lines[exec_sum_index:]
        except StopIteration:
             pass

        current_text = "\n".join(lines)
        
        if "## 1." in current_text and "## 2." in current_text:
             parts = current_text.split("## 2.")
             header_line = parts[0].split("\n", 1)[0]
             content_block = parts[0].split("\n", 1)[1].strip()
             wrapped_1 = f"{header_line}\n\n::: execsummary\n{content_block}\n:::\n\n"
             current_text = wrapped_1 + "## 2." + parts[1]

        if "## 8. Anexo Técnico" in current_text:
            parts = current_text.split("## 8. Anexo Técnico")
            header = "## 8. Anexo Técnico (Información de Respaldo)"
            content = parts[1].strip()
            current_text = parts[0] + f"{header}\n\n::: legalnotice\n{content}\n:::\n\n"

        full_printable = frontmatter + current_text
        
        printable_filename = f"PRINT_{base_name}.md"
        printable_filepath = os.path.join(self.REPORTS_DIR, printable_filename)
        
        with open(printable_filepath, 'w', encoding='utf-8') as f:
            f.write(full_printable)
            
        success, pdf_temp_path, error = self.pdf_converter.convert_to_pdf(printable_filepath)
        final_pdf_path = os.path.join(self.REPORTS_DIR, f"{base_name}.pdf")

        if success and pdf_temp_path and os.path.exists(pdf_temp_path):
             if os.path.exists(final_pdf_path):
                 os.remove(final_pdf_path)
             os.rename(pdf_temp_path, final_pdf_path)
             print(f"[+] PDF Report generated: {final_pdf_path}")
        else:
             print(f"[!] PDF Generation Error: {error}")
             
        if os.path.exists(printable_filepath):
            os.remove(printable_filepath)
            
        return final_pdf_path
            
        return final_pdf_path

    def cleanup_reports(self, client_name, current_scan_id):
        # Remove all MD/PDF reports for this client ensuring only the current one remains
        # Strategy: List all files for client, delete if not current_scan_id
        pattern = f"REPORT_{client_name}_*"
        files = glob.glob(os.path.join(OUTPUT_DIR, pattern))
        
        for f in files:
            # Check if it belongs to current scan
            if current_scan_id not in f:
                try:
                    os.remove(f)
                    print(f"[-] Cleanup: Removed old artifact {os.path.basename(f)}")
                except Exception as e:
                    print(f"[!] Cleanup Error: {e}")
