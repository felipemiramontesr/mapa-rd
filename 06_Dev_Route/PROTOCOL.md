# MAPA-RD Development Protocol (Golden Rules)

> [!IMPORTANT]
> These rules are MANDATORY for EVERY SINGLE ITERATION. No exceptions.

## 1. Security & Hygiene (.gitignore)
- **Action**: Check and update `.gitignore` in every step.
- **Goal**: Ensure no new temporary files, logs, or build artifacts provided by new tools are tracked.

## 2. Status Tracking (Checkpoint)
- **Action**: Update `Check_Points.md`.
- **Goal**: Reflect the exact status of the work immediately.

## 7.2 Escala de Riesgo (Etched in Stone)
Se define y CONGELA la siguiente escala de 5 niveles para todo el proyecto.
Cualquier desviación futura se considera un error crítico.

| Rango | Nivel | Color | Hex | Definición |
| :--- | :--- | :--- | :--- | :--- |
| **80-100** | MÁXIMO | 🟣 Púrpura | `#a29bfe` | Compromiso total inminente. |
| **60-79** | CRÍTICO | 🔴 Rojo | `#ff7675` | Daño severo confirmado. |
| **40-59** | ALTO | 🟠 Naranja | `#ff9f43` | Probabilidad alta de impacto. |
| **20-39** | MODERADO | 🟡 Amarillo | `#ffeaa7` | Riesgo latente o indirecto. |
| **00-19** | BAJO | 🔵 Azul | `#74b9ff` | Higiene o informativo. |

> [!IMPORTANT]
> El nivel **ALTO (40-59)** debe ser siempre **NARANJA**.
> No usar Rojo para Alto. Rojo es exclusivo de Crítico (60-79).

---

## 3. Business Logic Integrity (CI/CD)
- **Action**: Run `python 10_Tools/run_ci.py` (or `pipeline.py`).
- **Goal**: Validate that Unit Tests pass and Business Logic is preserved BEFORE confirming any task.

## 4. Continuous Synchronization (Push)
- **Action**: `git push origin main` after every relevant interaction.
- **Goal**: Ensure the remote repository is always up-to-date with the latest valid code.

## 5. Auto-Confirmation (File Saves)
- **Action**: Always default to "YES/ACCEPT" when the user asks about saving/updating a file.
- **Goal**: Eliminate redundant confirmation loops and speed up development.

## 6. Nomenclatura Final (Reportes)
> [!IMPORTANT]
> Strict naming convention for generated PDF files.

**Format**: MAPA-RD_<CLIENT_SLUG>_<CLIENT_ID>_<DOC_TYPE>_<SEQ>_<DATE>

**Example**: MAPA-RD_ACME-CORP_CL-0001_RPT_001_2026-01-11

**Filename**: MAPA-RD_ACME-CORP_CL-0001_RPT_001_2026-01-11.pdf

## 7. MAPA-RD Risk Methodology v1.0 (OFFICIAL)

> [!CAUTION]
> **VERSION LOCKED: v1.0**
> This methodology is FROZEN. 
> - No manual edits.
> - No subjective adjustments.
> - Changes require a FORMAL version increment (v1.1, v2.0).

### 7.0 Declaración Formal
Esta metodología es oficial y aplica a todos los reportes MAPA-RD.

**Incluye (Mandatorio):**
- **Metodología IRV**: Componentes, Escalas, Pesos, Normalización (0–100), Clasificación cromática radioactiva.
- **Metodología IRD**: Derivación exclusiva desde IRV, Cálculo ponderado por severidad.
- **Principios**: Objetividad, No edición manual, No ajuste subjetivo, Reproducibilidad.
- **Estrictamente Confidencial**: Todos los reportes generados contienen datos sensibles simulados o reales.
- **Fase HTML**: Durante esta fase, TODAS las modificaciones deben reflejarse únicamente en `C:/Felipe/Projects/Mapa-rd/report_engine/out/MAPA-RD_ACMECorpEXE20260111v10RPT-2026-001.html`. Ningún otro archivo de salida debe ser generado o modificado.idez histórica.

**Validación Histórica**: Los reportes generados bajo v1.0 conservan su validez histórica.

**Futuro (Roadmap):**
- *v1.1*: Podrá incluir ajustes de pesos y perfiles por industria.
- *v2.0*: Podrá incluir nuevos componentes y cambios estructurales.

### 7.1 Índice de Riesgo del Vector (IRV)
El Índice de Riesgo del Vector (IRV) mide la urgencia y el impacto real de NO cerrar un vector de vulnerabilidad identificado.

El IRV:
- Se calcula de forma interna.
- Se expresa en una escala normalizada de 0 a 100.
- No se edita manualmente.
- No se ajusta por percepción.
- No expone fórmulas ni pesos en el reporte final.

#### 7.1.1 Componentes del IRV (OBLIGATORIOS)
Cada Vector de Vulnerabilidad debe evaluarse usando los siguientes componentes:

1. **Criticidad del Activo (CA)** (0–5): Evalúa la criticidad del activo afectado.
2. **Exposición Temporal (ET)** (0–5): Evalúa si el vector es histórico, residual o activo.
3. **Superficie de Exposición (SE)** (0–5): Evalúa la facilidad de acceso al vector (interno → público).
4. **Impacto Multidimensional (IM)** (0–5): Suma de subimpactos binarios (0/1):
    - `impacto_personal`
    - `impacto_financiero`
    - `impacto_operativo`
    - `impacto_legal`
    - `impacto_integridad_fisica`
5. **Facilidad de Explotación (FE)** (0–5): Evalúa el esfuerzo técnico requerido para explotar el vector.
6. **Detectabilidad / Visibilidad (DV)** (0–5): Evalúa la probabilidad de que la explotación pase desapercibida.

#### 7.1.2 Pesos del Modelo IRV (v1.0)
Aplicar los siguientes pesos:
- CA × 4
- ET × 3
- SE × 3
- IM × 4
- FE × 3
- DV × 3

El resultado debe normalizarse a un rango de 0 a 100.

#### 7.1.3 Clasificación del IRV
| IRV | Nivel |
| :--- | :--- |
| 0–19 | Bajo |
| 20–39 | Medio |
| 40–59 | Alto |
| 60–79 | Crítico |
| 80–100 | Máximo |

#### 7.1.4 Clasificación Cromática Radioactiva (MANDATORIA)
Cada nivel IRV debe representarse visualmente usando la escala cromática radioactiva MAPA-RD:
- **Bajo** → Azul Radioactivo
- **Medio** → Amarillo Radioactivo
- **Alto** → Fucsia Radioactivo
- **Crítico** → Rojo Radioactivo
- **Máximo** → Púrpura Radioactivo

**Reglas:**
- El color NUNCA sustituye al valor numérico.
- El color siempre acompaña número + nivel textual.
- El color se usa solo como acento, no como fondo dominante.

### 7.2 Índice de Riesgo Digital (IRD)
El Índice de Riesgo Digital (IRD) representa el estado global de riesgo del entorno digital del cliente en un momento determinado.

El IRD:
- Se deriva exclusivamente de los IRV activos.
- No se calcula manualmente.
- No se ajusta subjetivamente.
- Se recalcula únicamente cuando cambian los IRV.

#### 7.2.1 Cálculo del IRD (MANDATORIO)
El IRD se calcula como un promedio ponderado por severidad de los IRV:

**Pesos por nivel IRV:**
- Bajo → ×1
- Medio → ×2
- Alto → ×3
- Crítico → ×4
- Máximo → ×5

**Fórmula conceptual:**
`IRD = Σ(IRV × peso) / Σ(pesos)`

Resultado normalizado: 0–100.

#### 7.2.2 Interpretación del IRD
| IRD | Nivel |
| :--- | :--- |
| 0–19 | Riesgo Bajo |
| 20–39 | Riesgo Moderado |
| 40–59 | Riesgo Alto |
| 60–79 | Riesgo Crítico |
| 80–100 | Riesgo Crítico Máximo |

### 7.3 Representación en Reportes
- Cada Vector muestra su IRV (valor + nivel).
- El IRD se muestra como indicador global del reporte.
- No se muestran fórmulas, pesos ni valores de componentes.
- El IRD debe indicar cuántos vectores se usaron para su cálculo.

### 7.4 Regla de Disciplina Operativa (CRÍTICA)
ANTES de CUALQUIER acción (código, diseño, lógica, contenido, naming):
1. **Revisar PROTOCOL.md completo.**
2. Verificar que la acción respeta todas las reglas vigentes.
3. Ejecutar Check_Points, CI y Push según el PROTOCOL.

**No seguir el PROTOCOL:**
- invalida la iteración
- introduce deuda técnica
- rompe la trazabilidad del sistema

**El PROTOCOL es mandatorio en CADA interacción.**
