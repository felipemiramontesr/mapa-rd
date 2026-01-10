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
| **Coverage** | 🔴 Red | Tests unitarios desactualizados o incompletos. |

---

## 📍 Roadmap & Hitos (Q1 2026)

### ✅ Hito 0: Fundamentos (Completado)
- [x] Análisis funcional del legado.
- [x] Refactorización de estructura de directorios (`00_Convention`).
- [x] Corrección de rutas críticas en `main.py` y módulos.
- [x] Verificación de ejecución básica (Smoke Test).

### 🚀 Hito 1: Integración Real (Sprint Actual)
**Objetivo:** Eliminar datos simulados y conectar motores reales.
- [ ] **INT-01**: Habilitar ejecución real de SpiderFoot (CLI/API).
- [ ] **INT-02**: Mapear salida JSON real de SpiderFoot al Normalizador.
- [ ] **CLI-01**: Implementar argumentos robustos en `main.py` para escaneos completos.

### ⚙️ Hito 2: Automatización y Escala
**Objetivo:** Permitir operación desatendida para múltiples clientes.
- [ ] **SCH-01**: Reparar `Scheduler` en `Orchestrator`.
- [ ] **DATA-01**: Implementar persistencia real (SQLite/TinyDB) para estados de intake.
- [ ] **NOT-01**: Validar envío de correos en entorno productivo.

---

## 📋 Product Backlog (Priorizado)

| ID | Prioridad | Tarea | Estado | Owner |
| :--- | :---: | :--- | :---: | :---: |
| **TECH-01** | 🔥 High | Reemplazar `mock_findings` en `orchestrator.py` con llamada a `sf_cli`. | To Do | Dev |
| **TECH-02** | ⚡ Med | Verificar manejo de errores si SpiderFoot no está instalado. | To Do | QA |
| **DOC-01** | ℹ️ Low | Crear diagrama de flujo de datos (Mermaid) en `README.md`. | To Do | Doc |
| **UX-01** | 🎨 Low | Mejorar template de correo HTML (actualmente texto plano/básico). | To Do | Design |

---

## 📝 Análisis de Situación Actual (Discovery)
*Preservado del reporte de análisis original para contexto.*

### Funcionalidades Completas
*   **Generación de Reportes**: Ejecutivos y ARCO (Markdown -> PDF).
*   **Gestión de Dependencias**: Instalación automática de Pandoc/MiKTeX.
*   **Notificaciones**: Módulo SMTP funcional.

### Deuda Técnica Crítica
1.  **SpiderFoot Mock**: El orquestador usa datos fijos. No hay recolección real.
2.  **Tests Frágiles**: Los tests dependen de rutas absolutas o mocks no actualizados.

---

## 🛠️ Recursos y Referencias
- **Ruta del Proyecto:** `c:\Felipe\Projects\Mapa-rd`
- **Configuración:** `03_Config/scan_profile.json`
- **Logs:** `04_Data/tracking/persistence.json` (Estado del sistema)
