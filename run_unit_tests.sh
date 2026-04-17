#!/usr/bin/env bash
# Script para ejecutar tests unitarios rápidamente (sin Ollama)

echo "🧪 Ejecutando Tests Unitarios (SIN Ollama requerido)"
echo "=================================================="
echo ""

# Tests unitarios del servicio
echo "📝 Tests del servicio OllamaConversationService..."
python -m pytest tests/test_ollama_service.py -v --tb=short

# Tests del endpoint
echo ""
echo "🔌 Tests del endpoint /ask..."
python -m pytest tests/test_ask_endpoint.py -v --tb=short

# Resumen
echo ""
echo "✅ Tests unitarios completados"
echo ""
echo "Para ejecutar tests de integración (requiere Ollama):"
echo "  pytest tests/test_ollama_integration.py -v"
echo ""
echo "Para ejecutar TODO:"
echo "  pytest tests/ -v"
echo ""
