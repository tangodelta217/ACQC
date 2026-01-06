# Arquitectura

Portal de arquitectura del sistema ACQC.

---

## Documentación

- [**Portal de Arquitectura**](ARCHITECTURE_PORTAL.md) — Vista completa: contexto, contenedores, despliegue, secuencias, estados y MLOps.

---

## Diagrama resumen

```mermaid
flowchart LR
  subgraph OT["OT (Purdue L0-L3)"]
    PLC["PLC/DCS"]
    PAT["PAT"]
  end
  
  subgraph DMZ["Industrial DMZ"]
    EDGE["Edge ACQC"]
  end
  
  subgraph IT["IT/Analytics"]
    MLO["MLOps"]
  end
  
  PLC -->|read-only| EDGE
  PAT --> EDGE
  MLO -->|deploy| EDGE
```

---

## Entregable relacionado

📄 [ACQC_Arquitectura.pdf](../00_Deliverables/ACQC_Arquitectura.pdf)
