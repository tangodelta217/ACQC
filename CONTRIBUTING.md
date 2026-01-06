# Contributing to ACQC

Gracias por el interés en contribuir a este proyecto.

## Principios

1. **Tono técnico e impersonal** — Evitar "nosotros" o lenguaje de marketing
2. **Sin datos sensibles** — No incluir nombres de sistemas reales no confirmados
3. **Resultados esperados, no medidos** — Este es un proyecto TFM, no producción
4. **Coherencia con SSOT** — Cualquier cambio debe reflejarse en `ssot/`

## Cómo contribuir

### Documentación

1. Fork del repositorio
2. Crear rama: `docs/descripcion-breve`
3. Editar archivos en `docs/`
4. Verificar: `mkdocs build --strict`
5. Abrir Pull Request

### SSOT (Tags, KPIs, Requisitos)

1. Crear issue usando template "SSOT Request"
2. Esperar aprobación de OT/QA según corresponda
3. Seguir proceso de PR con checklist

### Demo (src/)

1. Crear rama: `feat/descripcion-breve`
2. Mantener sin dependencias externas (stdlib Python)
3. Añadir tests para nuevas funcionalidades
4. Verificar: `pytest tests/ -v`

### Seguridad

- Usar template "Security Concern" para issues
- **No incluir detalles de explotación**
- Enfoque 100% defensivo

## Validación antes de PR

```bash
# Documentación
mkdocs build --strict

# Demo
cd src && pytest tests/ -v
```

## Estilo

- **Markdown**: Encabezados claros, párrafos cortos, tablas cuando aporten
- **Mermaid**: Diagramas simples y legibles
- **Python**: PEP 8, type hints, docstrings

## Preguntas

Abrir un issue con el template apropiado.
