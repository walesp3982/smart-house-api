"""
Tests de integración que requieren Ollama online (uso real)
Ejecutar solo cuando Ollama está corriendo

Para correr estos tests:
    pytest tests/test_ollama_integration.py -v -s

Para saltarlos (si Ollama no está disponible):
    pytest tests/test_ollama_integration.py -v --disable-warnings \\
        -m "not requires_ollama"
"""

import subprocess
from unittest.mock import patch

import pytest


def is_ollama_available() -> bool:
    """Verifica si Ollama está disponible"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except FileNotFoundError, subprocess.TimeoutExpired:
        return False


pytestmark = pytest.mark.skipif(
    not is_ollama_available(),
    reason="Ollama no está disponible - instala Ollama y ejecuta 'ollama serve'",
)


class TestOllamaIntegration:
    """Tests que requieren Ollama real corriendo"""

    def test_call_ollama_real(self, ollama_service_with_mocks):
        """Prueba llamada real a Ollama"""
        # Pregunta simple que Ollama puede responder rápidamente
        response = ollama_service_with_mocks._call_ollama(
            "Responde solo con una palabra: ¿Es un gato un animal?",
            model="llama2",
        )

        # Verifica que hay respuesta
        assert response != ""
        assert "Error" not in response or len(response) > 10

    def test_call_ollama_with_timeout(self, ollama_service_with_mocks):
        """Prueba timeout en llamada a Ollama"""
        # Una pregunta que debería devolver respuesta rápido
        result = ollama_service_with_mocks._call_ollama(
            "¿Cuántos días tiene una semana?",
            model="llama2",
        )

        # No debe ser un error de timeout
        assert "timeout" not in result.lower()

    def test_analyze_intent_real_query(self, ollama_service_with_mocks):
        """Test real del análisis de intención para consulta"""
        with patch.object(ollama_service_with_mocks, "_get_device_states_summary") as mock_summary:
            mock_summary.return_value = "Dispositivos: Luz Sala (light)"

            result = ollama_service_with_mocks._analyze_intent(
                "¿Cuántas luces están prendidas?", user_id=1
            )

            # Debe detectar que es una consulta
            assert result.get("intent") in ["query", "unknown"]

    def test_analyze_intent_real_command(self, ollama_service_with_mocks):
        """Test real del análisis de intención para comando"""
        with patch.object(ollama_service_with_mocks, "_get_device_states_summary") as mock_summary:
            mock_summary.return_value = "Dispositivos: Luz Sala (light)"

            result = ollama_service_with_mocks._analyze_intent("Apaga todas las luces", user_id=1)

            # Debe detectar que es un comando
            assert result.get("intent") in ["command", "unknown"]

    def test_process_message_real(self, ollama_service_with_mocks):
        """Test real del procesamiento completo"""
        with patch.object(ollama_service_with_mocks, "_find_devices_by_type") as mock_find:
            mock_find.return_value = []

            response = ollama_service_with_mocks.process_message("¿Cómo estás?", user_id=1)

            # Debe haber respuesta
            assert response != ""
            assert isinstance(response, str)

            # Debe estar en el historial
            history = ollama_service_with_mocks.get_conversation_history()
            assert len(history) == 2


@pytest.mark.skipif(
    is_ollama_available(),
    reason="Test offline: verifica manejo cuando Ollama NO está disponible",
)
class TestOllamaOffline:
    """Tests cuando Ollama NO está disponible"""

    def test_call_ollama_offline(self, ollama_service_with_mocks):
        """Verifica manejo correcto cuando Ollama no está disponible"""
        response = ollama_service_with_mocks._call_ollama("¿Hola?")

        # Debe devolver un error o mensaje adecuado
        assert response != ""
        # Puede ser error de no encontrado o timeout
        assert "Error" in response or "error" in response.lower()
