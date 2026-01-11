# MAPA-RD — ORDEN DE SERVICIO Y ONBOARDING
**Documento:** {doc_id} | **Versión:** {doc_version}
**Emitido:** {fecha_emision} {hora_emision} | **doc_uuid:** {doc_uuid}
**Clasificación:** {classification}

---

## 0. PORTADA Y CONTROL DOCUMENTAL
Este documento integra la Orden de Servicio y Onboarding del servicio MAPA-RD, incluyendo anexos vinculantes. Su uso es estrictamente confidencial.

## 1. PARTES
### 1.1 CLIENTE
**Nombre/Razón Social:** {cliente_nombre_razon} ({cliente_tipo_persona})
**RFC:** {cliente_rfc}
**Domicilio:** {cliente_domicilio}
**Contacto Notificaciones:** {cliente_correo_notificaciones} / {cliente_telefono_notificaciones}

{representante_section}

### 1.2 PROVEEDOR
**Nombre:** {provider_name}
**RFC:** {provider_rfc}
**Domicilio Fiscal:** {provider_address}
**Correo ARCO:** {provider_arco_email}

## 2. DECLARACIONES Y AUTORIZACIONES (OBLIGATORIO)
El Cliente declara, bajo protesta de decir verdad, que:
a) La información proporcionada en este documento y anexos es veraz, completa y actual.
b) Es titular de los activos listados en el Anexo A, o cuenta con facultades suficientes para autorizar su análisis y monitoreo.
c) Autoriza al Proveedor a realizar actividades de inteligencia en fuentes abiertas (OSINT) exclusivamente sobre fuentes públicas y sobre los activos autorizados.
d) Entiende que el servicio no implica intrusión, acceso no autorizado, ingeniería social, suplantación, explotación de vulnerabilidades, ni obtención ilícita de información.

**CASILLAS DE ACEPTACIÓN (OBLIGATORIO):**
- [{check_declaraciones}] ACEPTO Declaraciones y Autorizaciones (Sección 2)
- [{check_terminos}] ACEPTO Términos del Servicio (Secciones 3–14)
- [{check_privacidad}] ACEPTO Aviso de Privacidad versión {aviso_version} (Anexo C)
- [{check_secundarias}] ACEPTO finalidades secundarias (opcional)

## 3. DEFINICIONES (CORTAS)
- **Fuentes públicas:** información accesible sin autenticación ni permisos privados.
- **Hallazgo:** evidencia documentada de exposición o riesgo en fuentes públicas.
- **Incidente:** hallazgo con impacto relevante o urgencia (ver Sección 9).
- **Ruta de cierre:** plan de acciones y seguimiento hasta mitigación razonable.

## 4. OBJETO DEL SERVICIO
El Proveedor prestará el servicio MAPA-RD consistente en identificar, documentar y reportar exposición de información en fuentes públicas relacionada con los activos autorizados del Cliente, y entregar recomendaciones y, si aplica, acompañamiento documentado para gestión ARCO dentro del alcance contratado.

**Modalidad:** {modalidad_servicio}
**Frecuencia:** {frecuencia}
**Alcance:** {alcance}
**Nivel de detalle:** {nivel_detalle}
**Ventana de entrega:** {ventana_entrega_dias_habiles} días hábiles.

## 5. ALCANCE, LIMITACIONES Y PROHIBICIONES
5.1 **Alcance:** se limita estrictamente a los activos autorizados del Anexo A y a la configuración del Anexo B.
5.2 **Limitaciones:** el servicio se basa en fuentes públicas; por tanto, el Proveedor no garantiza eliminación total de información existente o futura, ni desindexación permanente en buscadores. Los resultados pueden variar por acciones de terceros.
5.3 **Prohibiciones:** el Proveedor no realizará intrusión, acceso no autorizado, ingeniería social, suplantación, explotación de vulnerabilidades ni actividades contrarias a la ley. Si el Cliente solicita actividades prohibidas, el Proveedor las rechazará y podrá terminar el servicio.

## 6. AUTORIZACIÓN DE ACTIVOS
El Cliente autoriza expresamente el análisis y monitoreo de los activos listados como “Autorizado = Sí” en el Anexo A. Cualquier activo no listado o no autorizado queda fuera del servicio.

## 7. ENTREGABLES Y EVIDENCIA
Entregables mínimos:
- Reporte Ejecutivo o Extendido según Anexo B.
- Tabla/Matriz de hallazgos (fuente, URL/ubicación, fecha/hora, descripción, severidad, recomendación).
- Ruta de cierre (cuando aplique).
La evidencia se documentará mediante enlaces y capturas. Cuando sea viable, se incluirá huella documental del reporte.

## 8. SLA, SOPORTE Y NOTIFICACIONES
**Canal de soporte:** {canal_soporte}
**Responsable operativo del Cliente:** {contacto_operativo_cliente}
**Notificaciones:** Se enviarán a {cliente_correo_notificaciones} y por el canal acordado en Anexo B.

## 9. INCIDENTES (SEVERIDAD Y TIEMPOS)
- **Severidad Alta:** riesgo inmediato o daño significativo (p. ej., suplantación activa, filtración crítica, fraude). Notificación en: {sla_incidente_alta}.
- **Severidad Media:** exposición relevante sin explotación inmediata confirmada. Notificación en: {sla_incidente_media}.
- **Severidad Baja:** exposición menor o informativa. Se integra al siguiente reporte.

## 10. DATOS PERSONALES, PRIVACIDAD Y ARCO
**Responsable:** el Proveedor.
**Finalidades:** prestación del servicio, soporte, cumplimiento legal.
**Conservación:** {retention_days} días posteriores a terminación.
**ARCO/Revocación:** solicitudes al correo {provider_arco_email} conforme Anexo C.

## 11. CONFIDENCIALIDAD
Vigencia: durante el servicio y {confidentiality_months} meses posteriores a la terminación.

## 12. PROPIEDAD INTELECTUAL
La metodología, plantillas y know-how permanecen como propiedad del Proveedor. El Cliente recibe licencia de uso interno no exclusiva sobre entregables.

## 13. CONDICIONES COMERCIALES, SUSPENSIÓN Y TERMINACIÓN
**Plan:** {plan} | **Precio:** {precio} {moneda} + impuestos.
**Periodicidad:** {periodicidad_pago} | **Forma de pago:** {forma_pago}
**Días de gracia:** {dias_gracia}
**Terminación:** Aviso de {aviso_terminacion_dias} días.

## 14. LEY APLICABLE, JURISDICCIÓN Y MISCELÁNEA
**Ley aplicable:** México. **Jurisdicción:** {jurisdiction_state}, {jurisdiction_city}.

---

## FIRMAS

| CLIENTE | PROVEEDOR |
|:---:|:---:|
| <br><br>___________________________ | <br><br>___________________________ |
| **Nombre:** {firma_cliente_nombre} | **Nombre:** {provider_name} |
| **Cargo:** {firma_cliente_cargo} | **RFC:** {provider_rfc} |
| **Fecha:** {firma_cliente_fecha} | **Fecha:** {firma_proveedor_fecha} |

---

## ANEXOS

### ANEXO A: ACTIVOS AUTORIZADOS
| Tipo | Identificador | Titularidad (Propio/Administrado/Tercero) | Autorizado | Observaciones |
|---|---|---|---|---|
{anexo_a_rows}

**ACUSE ANEXO A:**
“Confirmo que los activos marcados como ‘Autorizado = Sí’ son de mi titularidad o tengo facultades suficientes para autorizarlos para análisis y monitoreo en fuentes públicas (OSINT).”

- [ ] **Confirmo activos autorizados**
**Nombre:** {firma_cliente_nombre} | **Firma:** ___________________________ | **Fecha:** {firma_cliente_fecha}

---

### ANEXO B: CONFIGURACIÓN DEL SERVICIO
- **Modalidad:** {modalidad_servicio}
- **Frecuencia:** {frecuencia}
- **Alcance:** {alcance}
- **Nivel de detalle:** {nivel_detalle}
- **Ventana de entrega:** {ventana_entrega_dias_habiles} días hábiles
- **Canal soporte:** {canal_soporte}
- **Contacto operativo del cliente:** {contacto_operativo_cliente}
- **Canales de notificación:** {cliente_correo_notificaciones} + {canal_acordado}
- **Incidentes:** Alta={sla_incidente_alta}, Media={sla_incidente_media}, Baja=Integrado al próximo reporte

---

### ANEXO C: AVISO DE PRIVACIDAD (RESUMEN + ACUSE)
**AVISO DE PRIVACIDAD (RESUMEN) — Versión {aviso_version}**

**Responsable:** {provider_name}, RFC {provider_rfc}.
**Finalidades primarias:** prestación del servicio MAPA-RD, soporte, generación de reportes/evidencia y cumplimiento legal.
**Finalidades secundarias:** métricas internas y mejora del servicio sin divulgar información del Cliente.
**Transferencias/encargados:** uso de proveedores tecnológicos para almacenamiento y comunicaciones bajo obligaciones de confidencialidad y seguridad.
**Conservación:** {retention_days} días posteriores a la terminación, salvo obligación legal.
**ARCO/Revocación:** solicitudes al correo {provider_arco_email}
**Aviso completo:** {privacy_notice_url}

**ACUSE ANEXO C:**
- [ ] **He leído y acepto el Aviso de Privacidad versión {aviso_version}**
**Nombre:** {firma_cliente_nombre} | **Firma:** ___________________________ | **Fecha:** {firma_cliente_fecha}

---

### ANEXO D: GLOSARIO
- **Fuentes públicas:** Información accesible sin autenticación ni permisos privados.
- **Hallazgo:** Evidencia documentada de exposición o riesgo en fuentes públicas.
- **Incidente:** Hallazgo con impacto relevante o urgencia.
- **Severidad Alta:** Riesgo inmediato o daño significativo (ej. suplantación activa, filtración crítica).
- **Severidad Media/Baja:** Exposición relevante sin explotación inmediata o netamente informativa.
- **Ruta de cierre:** Plan de acciones y seguimiento hasta mitigación razonable.
- **Baseline / Recurrente:** Tipo de análisis (inicial exhaustivo vs monitoreo periódico).

---

### ANEXO E: SEGURIDAD, SUBENCARGADOS Y BRECHA
**Medidas mínimas de seguridad:**
- Control de acceso por roles y principio de mínimo privilegio.
- Segregación por cliente (separación lógica de datos).
- Cifrado en tránsito (TLS) y resguardo íntegro de evidencias.
- Backups y registro básico de accesos/acciones.

**Subencargados:** {subencargados}

**Notificación de brecha:**
“En caso de incidente de seguridad que comprometa confidencialidad/integridad de información del Cliente, el Proveedor notificará al contacto designado en un plazo máximo de {breach_notify_hours} horas desde su confirmación, por {canal_soporte} y correo de notificaciones.”

**Retención:**
“Retención de evidencia/datos: {retention_days} días posteriores a terminación.”

---

### ANEXO F: COMERCIAL Y DATOS FISCALES
**Condiciones Comerciales:**
- **Plan:** {plan} | **Precio:** {precio} {moneda}
- **Periodicidad:** {periodicidad_pago} | **Forma de pago:** {forma_pago}
- **Impuestos:** {impuestos} | **Días de gracia:** {dias_gracia}
- **Aviso terminación:** {aviso_terminacion_dias} días
- **Fecha inicio:** {fecha_inicio} | **Renovación:** {renovacion_cancelacion}

**Datos Fiscales del Proveedor:**
**Proveedor:** {provider_name}
**RFC:** {provider_rfc} | **Régimen:** {provider_tax_regime}
**Domicilio fiscal:** {provider_address}

---

## CONTROL DE INTEGRIDAD (FINAL)
**DOC_UUID:** {doc_uuid}
**SHA256 (Full Binary):** {sha256_full}
**ESTADO:** {classification}
