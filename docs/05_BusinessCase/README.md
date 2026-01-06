# Business Case & ROI

> Análisis económico basado en supuestos trazables, no en resultados medidos.

---

## Resumen ejecutivo

| Escenario | NPV esperado | Payback | Confianza |
|-----------|--------------|---------|-----------|
| **Pesimista** | Positivo (base × 0.7) | ~3 años | Baja |
| **Base** | Referencia | ~2 años | Media |
| **Optimista** | Base × 1.3 | ~1.5 años | Media |

!!! note "Importante"
    Estos valores son **proyecciones basadas en supuestos**. No representan resultados medidos en producción.

---

## Visualización

### NPV por escenario

![NPV Escenarios](../assets/roi_npv_scenarios.png)

### Payback por escenario

![Payback Escenarios](../assets/roi_payback_scenarios.png)

### Sensibilidad (±20% en 5 supuestos clave)

![Sensibilidad Tornado](../assets/roi_sensitivity_tornado.png)

---

## Fuentes de valor

| Categoría | Palanca | Supuesto clave |
|-----------|---------|----------------|
| **Calidad** | Reducción de off-spec | % scrap actual vs objetivo |
| **Energía** | Optimización de consumo | €/MWh × reducción esperada |
| **Throughput** | Menos paradas por variabilidad | Horas/año × coste oportunidad |
| **Lab** | Reducción de muestreos rutinarios | Coste/muestra × frecuencia |

---

## Estructura del Excel

El Business Case se mantiene en Excel para permitir auditoría de supuestos:

[:material-microsoft-excel: Descargar Excel](../00_Deliverables/09_BusinessCase_ROI_mejorado.xlsx){ .md-button .md-button--primary }

| Hoja | Contenido |
|------|-----------|
| `Resumen` | ROI/payback por escenario |
| `Supuestos` | Producción, energía, scrap, costes |
| `Beneficios_*` | Fórmulas por categoría |
| `Costes` | CAPEX/OPEX desglosado |
| `Sensibilidad` | ±20% en supuestos clave |
| `Trazabilidad` | Fuente de cada supuesto |

---

## Regla de trazabilidad

!!! warning "Requisito"
    Todo número debe tener:
    
    - Una **fuente** (documento, entrevista, histórico, tarifa), o
    - Un **supuesto explícito** con responsable y fecha de revisión

---

## Próximos pasos

1. **Validar supuestos** con stakeholders de planta
2. **Piloto shadow** para calibrar parámetros
3. **Actualizar modelo** con evidencia de piloto
4. **Decisión de escalado** basada en datos reales

---

## Referencias

- **Excel completo**: [`09_BusinessCase_ROI_mejorado.xlsx`](../00_Deliverables/09_BusinessCase_ROI_mejorado.xlsx)
- **KPIs de aceptación**: `ssot/kpi_acceptance.csv`
