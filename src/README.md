# ACQC Demo — Minimal Runnable Skeleton

> Demostración técnica del flujo de soft sensor con datos sintéticos.

---

## Qué hace

Este demo ejecuta un pipeline simplificado:

1. **Genera datos sintéticos** — Tags de proceso (temperatura, presión, flujo, analizador) con ruido y QC flags
2. **Ejecuta inferencia** — Soft sensor lineal (baseline) con incertidumbre calibrada
3. **Detecta OOD** — Marca predicciones fuera de rango esperado
4. **Genera audit log** — Trazabilidad completa de predicciones y decisiones

**Importante**: Este es un esqueleto demostrativo. No conecta a sistemas reales.

---

## Estructura

```
src/
├── acqc_demo/
│   ├── __init__.py
│   ├── __main__.py    # Entry point (CLI)
│   ├── data_gen.py    # Generador de datos sintéticos
│   ├── infer.py       # Soft sensor + predicción
│   └── trace.py       # Audit log
├── tests/
│   └── test_demo.py   # Suite de tests
├── pyproject.toml     # Configuración del proyecto
└── README.md          # Este archivo
```

---

## Ejecución rápida

### Sin instalación (desde src/)

```powershell
cd C:\Users\User\Desktop\ACQC\src

# Ejecutar el demo
python -m acqc_demo

# Con más samples y verbose
python -m acqc_demo -n 200 -v

# Especificar directorio de salida
python -m acqc_demo -o ./my_output
```

### Con instalación (opcional)

```powershell
cd C:\Users\User\Desktop\ACQC\src

# Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar en modo desarrollo
pip install -e .

# Ejecutar
acqc-demo
```

---

## Opciones CLI

| Opción | Descripción | Default |
|--------|-------------|---------|
| `-n`, `--samples` | Número de muestras a generar | 100 |
| `-o`, `--output` | Directorio de salida | `./output` |
| `-v`, `--verbose` | Mostrar predicciones de ejemplo | False |

---

## Salida esperada

```
============================================================
ACQC Demo - Soft Sensor Inference Skeleton
============================================================

[1/4] Generating synthetic data...
      Generated 100 samples
      Tags: TI-101, PI-201, FI-301, AI-401
      Data hash: abc123...

[2/4] Initializing soft sensor...
      Model ID: soft-sensor-ron-v1
      Version: 0.1.0-demo
      Model hash: def456...

[3/4] Running inference...
      Total predictions: 100
      OK: 95, DEGRADED: 3, OOD: 2
      Saved to: ./output/predictions.json

[4/4] Generating audit log...
      Entries: {'PREDICTION': 100, 'RECOMMENDATION': 95, 'DECISION': 1}
      Saved to: ./output/audit/audit_log.json

============================================================
Demo completed successfully!
============================================================
```

---

## Archivos generados

| Archivo | Contenido |
|---------|-----------|
| `output/data/dataset.json` | Datos sintéticos (tags + calidad) |
| `output/predictions.json` | Predicciones del soft sensor |
| `output/audit/audit_log.json` | Log de trazabilidad |

---

## Tests

```powershell
cd C:\Users\User\Desktop\ACQC\src

# Instalar pytest (si no está)
pip install pytest

# Ejecutar tests
pytest tests/ -v

# Con cobertura
pip install pytest-cov
pytest tests/ --cov=acqc_demo --cov-report=term-missing
```

---

## Dependencias

**Runtime**: Solo biblioteca estándar de Python 3.10+

**Desarrollo**:
- `pytest>=7.0`
- `pytest-cov>=4.0`

---

## Relación con la arquitectura

Este demo implementa de forma simplificada:

| Componente arquitectura | Implementación demo |
|------------------------|---------------------|
| Edge collector | `data_gen.py` (simulado) |
| Feature pipeline | Incluido en `data_gen.py` |
| Soft sensor service | `infer.py` |
| Drift/OOD detection | `infer.py` (simplificado) |
| Audit log | `trace.py` |

Ver [Portal de Arquitectura](../docs/01_Architecture/ARCHITECTURE_PORTAL.md) para la arquitectura completa.
