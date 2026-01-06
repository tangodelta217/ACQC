# Demo Story — Guion de 2-3 minutos

> Guion para presentar ACQC a perfiles técnicos y de gestión sin requerir resultados medidos.

---

## Antes de empezar

!!! tip "Preparación"
    - Tener abierto el portal en navegador
    - One-Pager PDF listo para proyectar
    - Excel de Business Case disponible

---

## Guion con checkpoints

### ⏱️ 0:00–0:30 | Apertura

**Mensaje clave**: *"Incremento de variabilidad por materias primas circulares → necesidad de estimación online de calidad."*

- [ ] Mencionar contexto: presión sobre energía y calidad
- [ ] Objetivo: reducir incertidumbre operacional

---

### ⏱️ 0:30–1:00 | Qué es ACQC

**Abrir**: [Home del portal](../index.md)

- [ ] Mostrar diagrama "Arquitectura at a glance"
- [ ] Destacar: **solo lectura de OT** (no hay control automático)
- [ ] Mencionar los 3 pilares: soft sensors, advisory, MLOps

---

### ⏱️ 1:00–1:45 | Cómo funciona

**Abrir**: [Architecture Portal](../01_Architecture/ARCHITECTURE_PORTAL.md)

- [ ] Mostrar secuencia de operación (inferencia → drift → recomendación)
- [ ] Mostrar máquina de estados: Normal → Degradado → Suspendido
- [ ] Enfatizar: *"Cuando no es seguro recomendar, el sistema lo dice"*

---

### ⏱️ 1:45–2:15 | Validación y Governance

**Abrir**: [Governance](../03_Governance/index.md)

- [ ] Mostrar tabla de gates (Gate 0 → Gate N)
- [ ] Mencionar: versionado, rollback, auditoría
- [ ] Referencia a validación contra laboratorio

---

### ⏱️ 2:15–2:45 | Business Case

**Abrir**: [Business Case](../05_BusinessCase/README.md) o [Home](../index.md)

- [ ] Mostrar gráfico NPV por escenario
- [ ] Mostrar sensibilidad ±20%
- [ ] Mensaje: *"Caso económico basado en supuestos trazables"*

---

### ⏱️ 2:45–3:00 | Cierre

**Próximo paso natural**:

- [ ] Piloto en modo **shadow** (solo monitorización)
- [ ] Campaña de muestreo para evidencia
- [ ] Decisión de escalado basada en datos

---

## Checkpoint final

| ✓ | Punto clave comunicado |
|---|------------------------|
| ☐ | Solo lectura, no control automático |
| ☐ | Operador/a decide, sistema recomienda |
| ☐ | Gobernanza completa (gates, rollback) |
| ☐ | Business case con supuestos trazables |
| ☐ | Próximo paso: piloto shadow |

---

## Referencias rápidas

| Recurso | Enlace |
|---------|--------|
| One-Pager PDF | [Descargar](../00_Deliverables/ACQC_OnePager.pdf) |
| Arquitectura | [Portal](../01_Architecture/ARCHITECTURE_PORTAL.md) |
| MLOps Gates | [Governance](../03_Governance/index.md) |
| Business Case | [ROI](../05_BusinessCase/README.md) |
| Validación | [PDF](../00_Deliverables/ACQC_Validacion.pdf) |
