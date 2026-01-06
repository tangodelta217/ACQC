# Runbook — Respuesta a incidentes (ACQC)

## Principio
Ante duda, **se congela recomendación** y se mantiene monitorización hasta restablecer evidencias.

## Señales típicas de incidente
- Drift/OOD persistente.
- Pérdida de conectividad (OPC UA/historian/PAT).
- Integridad comprometida (hash/firma no válida).
- Latencia degradada.
- Falta de trazabilidad (logs incompletos).

## Acciones inmediatas
1. Cambiar a estado **Suspendido** (bloquear advisory).
2. Capturar snapshot: versión de modelo, hashes, config, ventana de datos.
3. Notificar: OT/QA/Seguridad según criticidad.
4. Ejecutar rollback a último paquete firmado.

## Evidencias mínimas (auditoría)
- `event_id`, timestamp, versión, hash artefactos, motivo, operador responsable.
