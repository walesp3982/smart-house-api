# Script para ejecutar tests unitarios rápidamente (sin Ollama)
# Uso: .\run_unit_tests.ps1

Write-Host "🧪 Ejecutando Tests Unitarios (SIN Ollama requerido)" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Activar venv si existe
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activando virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
}

# Tests unitarios del servicio
Write-Host "📝 Tests del servicio OllamaConversationService..." -ForegroundColor Green
python -m pytest tests/test_ollama_service.py -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests unitarios pasaron" -ForegroundColor Green
} else {
    Write-Host "❌ Tests unitarios fallaron" -ForegroundColor Red
    exit 1
}

# Tests del endpoint
Write-Host ""
Write-Host "🔌 Tests del endpoint /ask..." -ForegroundColor Green
python -m pytest tests/test_ask_endpoint.py -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests del endpoint pasaron" -ForegroundColor Green
} else {
    Write-Host "❌ Tests del endpoint fallaron" -ForegroundColor Red
    exit 1
}

# Resumen
Write-Host ""
Write-Host "✅ Todos los tests unitarios completados" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar tests de integración (requiere Ollama):" -ForegroundColor Yellow
Write-Host "  pytest tests/test_ollama_integration.py -v" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para ejecutar TODO:" -ForegroundColor Yellow
Write-Host "  pytest tests/ -v" -ForegroundColor Yellow
Write-Host ""
