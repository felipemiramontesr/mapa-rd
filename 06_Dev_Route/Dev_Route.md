# 🗺️ Dev Route: MAPA-RD (Delivery Roadmap)

> **Documento Vivo de Seguimiento del Proyecto**
> **Versión:** 1.0.0
> **Estado:** 🚧 Refactoring / Beta Stabilization
> **Delivery Manager:** Virtual Agent

---

## 🚦 Executive Status (RAG)
| Componente | Estado | Notas |
| :--- | :---: | :--- |
| **Arquitectura** | 🟢 Green | Estructura de directorios refactorizada y modular. |
| **Core Engine** | 🟡 Amber | Generación de reportes sólida; Inteligencia simulada (Mock). |
| **CLI / Entry** | 🟢 Green | Reparado y verificado (Smoke Test OK). |
| **Coverage** | � Green | Test suite expandido y dashboard operativo. |

---

## 📍 Roadmap & Hitos (Q1 2026)

### ✅ Hito 0: Fundamentos (Completado)
- [x] Análisis funcional del legado.
- [x] Refactorización de estructura de directorios (`00_Convention`).
- [x] Corrección de rutas críticas en `main.py` y módulos.
- [x] Verificación de ejecución básica (Smoke Test).

### 🚀 Hito 1: Integración Real (Sprint Actual)
**Objetivo:** Eliminar datos simulados y conectar motores reales.
- [x] **INT-01**: Habilitar ejecución real de SpiderFoot (CLI/API).
- [x] **INT-02**: Mapear salida JSON real de SpiderFoot al Normalizador.
- [x] **NOT-01**: Validar envío de correos SMTP en entorno productivo (Con copia a Admin).
- [x] **CLI-01**: Implementar argumentos robustos en `main.py` para escaneos completos.

### ⚙️ Hito 2: Automatización y Escala
**Objetivo:** Permitir operación desatendida para múltiples clientes.
- [ ] **DATA-01**: Adquirir API KEY de HIBP (HaveIBeenPwned) para datos reales.
- [ ] **SCH-01**: Automatizar escaneo recurrente validado con datos reales.
- [ ] **UX-01**: Mejorar template de correo HTML (actualmente texto plano mejorado).

---

## 🛑 CHECKPOINT (2026-01-09)
**Estado:** El sistema es funcional de punta a punta (Pipeline, PDF, Email), pero SpiderFoot gratuito entrega "0 hallazgos" para correos reales, lo que genera reportes vacíos que el QC bloquea correctamente.

**Acción Requerida para Retomar:**
1.  **FINANCIAMIENTO:** Adquirir API Key de HaveIBeenPwned ($4.50 USD).
2.  **CONFIGURACIÓN:** Agregar la key a SpiderFoot.
3.  **PRUEBA FINAL:** Re-ejecutar escaneo de *Ana Flores*.

**Lista Prioritaria de Módulos (Orden de Impacto):**
Esta lista define en qué gastar para maximizar el valor del reporte (Detalles en `API_Investment_Plan.md`):

1.  🥇 **HaveIBeenPwned (HIBP)** | ~$4.50/mes | *CRÍTICO para detectar leaks de contraseñas.*
2.  🥈 **Google Custom Search API** | Freemium | *Crucial para búsquedas de nombres/redes sociales.*
3.  🥉 **DeHashed** | ~$5/semana | *Alto valor: muestra las contraseñas reales (no solo el aviso).*
4.  **Shodan** | ~$49/mes | *Infraestructura (IPs/Cámaras). Prioridad baja para Personas Físicas.*
5.  **Hunter.io** | Freemium | *Corporativo. Útil para empresas, no para personales.*

---

## 📋 Product Backlog (Priorizado)

| ID | Prioridad | Tarea | Estado | Owner |
| :--- | :---: | :--- | :---: | :---: |
| **DATA-01** | 🔥 High | **Comprar y Configurar API HIBP** | Blocked | User |
| **TECH-02** | ⚡ Med | Verificar manejo de errores si SpiderFoot no está instalado. | Done | QA |
| **DOC-01** | ℹ️ Low | Crear diagrama de flujo de datos (Mermaid) en `README.md`. | Done | Doc |

---

## 📝 Análisis de Situación Actual (Discovery)
*Preservado del reporte de análisis original para contexto.*

### Funcionalidades Completas
*   **Pipeline Completo**: Intake -> SF (Real) -> PDF -> QC -> Email.
*   **Generación de Reportes**: Ejecutivos y ARCO (Markdown -> PDF).
*   **Notificaciones**: SMTP real configurado y probado.

### Deuda Técnica Crítica
1.  **Falta de Datos Reales**: Se requiere inversión en APIs (HIBP) para que el motor SpiderFoot sea efectivo comercialmente.

---

## 🛠️ Recursos y Referencias
- **Ruta del Proyecto:** `c:\Felipe\Projects\Mapa-rd`
- **Plan de Inversión:** `06_Dev_Route/API_Investment_Plan.md`
- **Logs:** `04_Data/tracking/persistence.json` (Estado del sistema)
