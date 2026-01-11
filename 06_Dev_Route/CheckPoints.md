# 🏁 Check-Points & Roadmap: MAPA-RD

> **Propósito:** Este documento es el "punto de retorno" para entender rápidamente el estado del proyecto, qué se ha logrado y qué sigue.

## 📅 Estado al: 10 de Enero, 2026
**Estado Global:** 🟡 **BLOQUEADO (Fuentes de Datos)**
**Última Versión:** 1.0.0 (Beta Stabilization)

---

## 🏗️ De dónde venimos (Logros)
- [x] **Fase 1: Testing & Bug Fixing (COMPLETADA):** Notifier reparado. suite de 7 tests pasando al 100%.
- [x] **Fase 2: Refactorización Core (COMPLETADA):**
    - [x] **StateManager**: Migrado a arquitectura basada en tipos, Google Docstrings y validaciones robustas.
    - [x] **Orchestrator**: Lógica de pipeline profesionalizada con manejo de errores y rutas deterministas.
    - [x] **Normalizer/Scorer/Deduper**: Documentados y tipados bajo estándares PEP 484.
    - [x] **QCManager**: Motor de validación strict v2.3 implementado.
- [x] **Fase 3: CI/CD Pipeline (COMPLETADA):**
    - [x] Implementación de GitHub Actions (`ci.yml`) con Linting (flake8), Seguridad (bandit) y Testing (pytest).
    - [x] Estandarización de entorno con `requirements.txt`.
- [x] **Fase 4: Git & Privacidad (COMPLETADA):** .gitignore optimizado para proteger datos de clientes.
- [x] **Phase 5: Professional Coding Standards** - Refactoring Core, Docstrings, and CI/CD Cleanup.
- [x] **Phase 5.1: CI/CD Stabilization** - Fixed Flake8/Bandit compliance, removed legacy code, and greenlit Pipeline.
- [ ] **Phase 6: External Integrations** - HIBP API & Google Search.
- [x] **Phase 5.1: CI/CD Stabilization** - Fixed Flake8/Bandit compliance, removed legacy code, and greenlit Pipeline.
- [ ] **Phase 6: External Integrations** - HIBP API & Google Search.
    - [x] **Refactorización Senior**: Aplicación de Type Hints, Docstrings estilo Google y manejo de excepciones robusto en todo el core.
    - [x] **Comentarización Pro**: Documentación interna detallada en `normalizer`, `deduper`, `scorer`, `test_pipeline` y `dashboard`.
    - [x] **Testing Robusto**: Suite de pruebas integral validando el ciclo de vida completo.

---

## 🚧 En qué estamos (Haciendo / Sprint Actual)
*   **Estado Global:** 🟢 **COMPLETADO (Reporte V90 Finalizado)**
*   **Foco Actual:** Implementación final de secciones de Impacto y Localización al 100%.

### 🏆 Logros de la Sesión (V80 -> V90):
*   **V83:** Restauración Premium UI & Datos Dinámicos.
*   **V84:** Mitigación Contextual (Pasos inteligentes según tipo de dato).
*   **V86:** Localización al Español (UI & Inyección de Metadatos).
*   **V88:** Corrección de Lógica de Riesgo (Contraseñas = Crítico).
*   **V89:** Secciones de Impacto (Línea de Tiempo & Kill Chain).
*   **V90:** Desglose de "Factura Dark Web" (Valor de Mercado Detallado).

---

## 📋 Roadmap de Tareas

### 🔴 Por Hacer (Alta Prioridad)
- [ ] **DATA-01: Inversión HIBP:** Adquirir API Key de Provide HaveIBeenPwned ($4.50). Sin esto, el reporte no detecta lo más valioso (leaks).
- [ ] **CONFIG-01: Google OSINT:** Configurar la API de Google Custom Search (Capa gratuita) para detectar perfiles sociales.
- [ ] **TEST-01: Validación Ana Flores:** Re-ejecutar el pipeline para el usuario de prueba una vez activas las llaves.

### 🔵 Próximos Pasos (Media Prioridad)
- [ ] **UI-01: Premium Email:** Convertir el template de correo actual a uno HTML con diseño de marca.
- [ ] **PROC-02: Deduplicación Avanzada:** Refinar el `Deduper` para limpiar hallazgos redundantes entre distintos módulos de SpiderFoot.

---

## ⚠️ Riesgos y Alertas
| Riesgo | Impacto | Mitigación |
| :--- | :--- | :--- |
| **Reportes Vacíos** | 🔥 Alto | El QC ya los bloquea, pero la solución real es pagar la API de HIBP. |
| **Límites de API** | 🟡 Medio | Usar Google Search solo para lo indispensable y monitorear cuotas. |
| **Falsos Positivos** | 🟢 Bajo | El `Scorer` debe ser ajustado conforme lleguen datos reales. |

---

## 💡 Tips para Retomar el Vuelo (Developer Handover)
1.  **¿Cómo probar?**: Ejecuta `python main.py --client ana-flores --type baseline`.
2.  **Rutas Clave**:
    - Código: `07_Src/`
    - Resultados: `04_Data/reports/` (Ignorados en Git, ver localmente).
    - Configuración: `03_Config/config.json` (Aquí van las futuras API Keys).
3.  **Estado Crítico**: Si ves un error de QC, es porque SpiderFoot no encontró nada. Revisa `04_Data/raw/[ID]/spiderfoot.json` para confirmar que el archivo está vacío o tiene pocos datos.

---

## 🏆 Próximo Hito: "First Value Report"
**Objetivo:** Generar el primer reporte con hallazgos reales de filtraciones de contraseñas.
