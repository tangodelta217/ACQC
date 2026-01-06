# ACQC Demo Runner (PowerShell)
# Ejecuta el demo con configuración por defecto

$ErrorActionPreference = "Stop"

Write-Host "ACQC Demo Runner" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio src
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcDir = Join-Path (Split-Path -Parent $scriptDir) "src"

Push-Location $srcDir

try {
    # Verificar Python
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
    
    # Ejecutar demo
    Write-Host ""
    Write-Host "Ejecutando demo..." -ForegroundColor Yellow
    Write-Host ""
    
    python -m acqc_demo -n 50 -v
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Demo completado exitosamente!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Error en la ejecucion del demo" -ForegroundColor Red
        exit 1
    }
}
finally {
    Pop-Location
}
