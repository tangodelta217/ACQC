# Release Notes — ACQC v1.0.0

> Primera versión del repositorio de documentación y demo para ACQC.

---

## Capacidades incluidas

### 📚 Portal de Documentación (MkDocs)

- **Home** con resumen ejecutivo y navegación rápida
- **Arquitectura** con diagramas Mermaid (contexto, contenedores, deploy, estados)
- **Traceability Story** completo (dato → decisión)
- **Governance/MLOps** con tabla de gates G0-G5
- **Security** con threat model y controles por capa
- **Business Case** con visualizaciones NPV/Payback

### 🔧 Demo Ejecutable (src/)

- Generador de datos sintéticos (tags + calidad)
- Soft sensor baseline con incertidumbre
- Detección OOD simplificada
- Audit log con trazabilidad completa
- Suite de tests pytest

### 📊 SSOT (Single Source of Truth)

- Tag dictionary template
- Quality variables
- Requirements matrix
- KPI acceptance criteria
- Risk register

### 🔄 CI/CD

- Markdown link check
- MkDocs build strict
- Python tests
- Dependabot (GitHub Actions + Python)
- GitHub Pages deployment

### 📝 GitHub Polish

- Issue templates (Bug, SSOT Request, QA Evidence, Security)
- PR template con checklist
- CONTRIBUTING.md
- CODEOWNERS

---

## Estructura del repositorio

```
ACQC/
├── .github/           # Workflows, templates, config
├── docs/              # Portal MkDocs
├── src/               # Demo ejecutable
├── ssot/              # Single Source of Truth
├── schemas/           # Contratos de datos JSON
├── runbooks/          # Procedimientos operativos
├── scripts/           # Utilidades
├── mkdocs.yml         # Config del portal
├── README.md          # Entrada principal
└── CONTRIBUTING.md    # Guía de contribución
```

---

## Próximos pasos sugeridos

1. ~~Reemplazar `<usuario>` por el usuario real de GitHub~~ ✅ `tangodelta217`
2. Push a GitHub y verificar CI verde
3. Activar GitHub Pages (Settings → Pages → Source: GitHub Actions)
4. Demo de pasillo con el guion de 2-3 minutos

---

## Limitaciones conocidas

- **Sin datos reales**: Todo es sintético/template
- **Sin resultados medidos**: Solo "resultados esperados"
- **Demo skeleton**: No es código de producción
