# PLAN DE INVERSIÓN: Módulos de Pago para MAPA-RD
**Fecha:** 2026-01-09
**Objetivo:** Maximizar la detección de riesgos de identidad con el menor costo posible.

Esta lista prioriza los módulos según su **IMPACTO DIRECTO** en el modelo de negocio de MAPA-RD (foco en Personas Físicas, Correos, Contraseñas y Reputación).

---

## 🟢 NIVEL 1: CRÍTICOS (Must Have) 
*Sin esto, el servicio no detecta fugas de contraseñas confiables.*

### 1. **HaveIBeenPwned (HIBP)**
*   **Impacto:** 10/10 (El núcleo del servicio).
*   **Qué hace:** Detecta en qué bases de datos filtradas (leaks) aparece el correo.
*   **Costo:** **$4.50 USD / mes**.
*   **Módulo SF:** `sfp_haveibeenpwned`
*   **Por qué pagar:** Es la fuente más grande y fiable del mundo. Sin ella, estamos ciegos ante leaks masivos.

---

## 🟡 NIVEL 2: ALTO VALOR (Should Have)
*Mejoran drásticamente la búsqueda de personas y datos técnicos.*

### 2. **SocialSearcher / Google Custom Search JSON API**
*   **Impacto:** 8/10 (Ingeniería social).
*   **Qué hace:** Permite buscar menciones del nombre/usuario en redes sociales y web abierta sin bloqueos de CAPTCHA.
*   **Costo:** 
    *   **Google:** Gratis hasta 100 consultas/día (suficiente para iniciar). $5 USD por cada 1k extras.
    *   **SocialSearcher:** Planes desde ~30 EUR/mes (Opcional, Google suele bastar al inicio).
*   **Módulo SF:** `sfp_google` / `sfp_bing` (Requieren API Keys para evitar bloqueos).
*   **Recomendación:** Configurar la **capa gratuita de Google** Cloud Console.

### 3. **DeHashed** (o LeakIX)
*   **Impacto:** 8/10 (Detalle de contraseñas).
*   **Qué hace:** A diferencia de HIBP (que te dice "se filtró"), DeHashed a veces te muestra **cuál** fue la contraseña filtrada (o su hash). Eso impacta mucho al cliente.
*   **Costo:** ~$5.49 USD / 1 semana (puro ad-hoc) o ~$150 USD/año.
*   **Módulo SF:** `sfp_tool_dehashed` (o uso manual integrado).

---

## 🟠 NIVEL 3: INFRAESTRUCTURA (Nice to Have - Empresas)
*Más útil si vendes a empresas (PM) que a personas (PF).*

### 4. **Shodan**
*   **Impacto:** 6/10 (Para PF), 9/10 (Para Empresas).
*   **Qué hace:** Escanea IPs, Routers, Cámaras, Servidores.
*   **Costo:** **$49 USD / mes** (Membership de por vida a veces sale en oferta por $50 USD una sola vez en Black Friday).
*   **Módulo SF:** `sfp_shodan`.

### 5. **Hunter.io**
*   **Impacto:** 7/10 (Corporativo).
*   **Qué hace:** Encuentra la estructura de correos de una empresa `@dominio.com`.
*   **Costo:** Gratis (25 búsquedas/mes). Planes desde **$49 USD / mes**.
*   **Módulo SF:** `sfp_hunter`.

---

## ⚪ NIVEL 4: INTELIGENCIA DE AMENAZAS (Avanzado)
*Solo si gestionas ciberseguridad defensiva activa.*

### 6. **VirusTotal**
*   **Impacto:** 5/10 (Reputación).
*   **Qué hace:** Dice si un archivo/dominio es malware.
*   **Costo:** **Gratis** (API Pública limitada, suficiente para MAPA-RD). **PREMIUM** cuesta miles de dólares (Enterprise).
*   **Módulo SF:** `sfp_virustotal`.

### 7. **BuiltWith**
*   **Impacto:** 4/10.
*   **Qué hace:** Perfil tecnológico de un sitio web.
*   **Costo:** Gratis limitado. Planes desde $295 USD/mes (Muy caro, no prioritario).
*   **Módulo SF:** `sfp_builtwith`.

---

## 💰 RESUMEN PRESUPUESTO INICIAL (BOOTSTRAP)

Para lanzar el servicio **mañana** con calidad profesional:

1.  **HIBP:** $4.50 USD / mes.
2.  **Google Custom Search:** $0.00 (Usando capa Free Tier).
3.  **VirusTotal:** $0.00 (Usando capa Free Public).
4.  **Shodan:** $0.00 (Plan básico free user).

**TOTAL MENSUAL REQUERIDO: $4.50 USD.**

El resto se puede ir agregando conforme ganes clientes.
