"""
Tests para OllamaConversationService con mocks
No requiere Ollama online - todos los tests usan mocks
"""

import json
from unittest.mock import patch


class TestOllamaServiceWithoutServer:
    """Tests que NO requieren Ollama corriendo (usa mocks)"""

    def test_call_ollama_mocked(self, ollama_service_with_mocks):
        """Prueba que _call_ollama funciona con mock de subprocess"""
        with patch("app.services.ollama.subprocess.run") as mock_run:
            mock_run.return_value.stdout = "Respuesta simulada"
            mock_run.return_value.returncode = 0

            result = ollama_service_with_mocks._call_ollama("¿Hola?")

            assert "simulada" in result
            mock_run.assert_called_once()

    def test_call_ollama_timeout(self, ollama_service_with_mocks):
        """Prueba manejo de timeout"""
        with patch("app.services.ollama.subprocess.run") as mock_run:
            import subprocess as sp

            mock_run.side_effect = sp.TimeoutExpired("cmd", 30)

            result = ollama_service_with_mocks._call_ollama("¿Hola?")

            assert "Error" in result
            assert "tardó demasiado" in result

    def test_call_ollama_file_not_found(self, ollama_service_with_mocks):
        """Prueba cuando Ollama no está instalado"""
        with patch("app.services.ollama.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            result = ollama_service_with_mocks._call_ollama("¿Hola?")

            assert "Ollama no está instalado" in result

    def test_get_device_states_summary_no_devices(
        self, ollama_service_with_mocks, mock_installed_device_service
    ):
        """Prueba resumen cuando no hay dispositivos"""
        mock_installed_device_service.get_all_with_device.return_value = []

        result = ollama_service_with_mocks._get_device_states_summary(user_id=1)

        assert "No hay dispositivos" in result

    def test_get_device_states_summary_with_devices(
        self,
        ollama_service_with_mocks,
        mock_installed_device_service,
        sample_light_device,
    ):
        """Prueba resumen con dispositivos"""
        mock_installed_device_service.get_all_with_device.return_value = [sample_light_device]

        result = ollama_service_with_mocks._get_device_states_summary(user_id=1)

        assert "Luz Sala" in result
        assert "light" in result

    def test_analyze_intent_query(self, ollama_service_with_mocks):
        """Prueba análisis de intención para consulta"""
        with patch.object(ollama_service_with_mocks, "_call_ollama") as mock_call:
            mock_call.return_value = json.dumps(
                {
                    "intent": "query",
                    "device_types": ["light"],
                    "action": None,
                    "description": "Consultar luces",
                }
            )

            result = ollama_service_with_mocks._analyze_intent("¿Cuántas luces?", user_id=1)

            assert result["intent"] == "query"
            assert "light" in result["device_types"]

    def test_analyze_intent_command(self, ollama_service_with_mocks):
        """Prueba análisis de intención para comando"""
        with patch.object(ollama_service_with_mocks, "_call_ollama") as mock_call:
            mock_call.return_value = json.dumps(
                {
                    "intent": "command",
                    "device_types": ["light"],
                    "action": "off",
                    "description": "Apagar luces",
                }
            )

            result = ollama_service_with_mocks._analyze_intent("Apaga todo", user_id=1)

            assert result["intent"] == "command"
            assert result["action"] == "off"

    def test_analyze_intent_invalid_json(self, ollama_service_with_mocks):
        """Prueba cuando Ollama devuelve JSON inválido"""
        with patch.object(ollama_service_with_mocks, "_call_ollama") as mock_call:
            mock_call.return_value = "Esto no es JSON válido"

            result = ollama_service_with_mocks._analyze_intent("¿Hola?", user_id=1)

            assert result["intent"] == "unknown"
            assert result["action"] is None

    def test_find_devices_by_type(
        self,
        ollama_service_with_mocks,
        mock_installed_device_service,
        sample_light_device,
        sample_door_device,
    ):
        """Prueba búsqueda de dispositivos por tipo"""
        mock_installed_device_service.get_all_with_device.return_value = [
            sample_light_device,
            sample_door_device,
        ]

        result = ollama_service_with_mocks._find_devices_by_type(user_id=1, device_types=["light"])

        assert len(result) == 1
        assert result[0].name == "Luz Sala"

    def test_execute_command_on_device(self, ollama_service_with_mocks, sample_light_device):
        """Prueba ejecución de comando en dispositivo"""
        result = ollama_service_with_mocks._execute_command_on_device(
            sample_light_device, "on", user_id=1
        )

        assert isinstance(result, bool)
        ollama_service_with_mocks.mqtt_provider.publish.assert_called_once()

    def test_execute_command_invalid_action(self, ollama_service_with_mocks, sample_light_device):
        """Prueba comando con acción inválida"""
        result = ollama_service_with_mocks._execute_command_on_device(
            sample_light_device, "invalid", user_id=1
        )

        assert result is False

    def test_generate_response_query_no_devices(self, ollama_service_with_mocks):
        """Prueba generación de respuesta para consulta sin dispositivos"""
        intent_analysis = {
            "intent": "query",
            "device_types": ["light"],
            "action": None,
            "description": "Consultar luces",
        }

        with patch.object(ollama_service_with_mocks, "_find_devices_by_type") as mock_find:
            mock_find.return_value = []

            response = ollama_service_with_mocks._generate_response(intent_analysis, user_id=1)

            assert "No encontré dispositivos" in response

    def test_generate_response_command_applied(
        self, ollama_service_with_mocks, sample_light_device
    ):
        """Prueba generación de respuesta para comando ejecutado"""
        intent_analysis = {
            "intent": "command",
            "device_types": ["light"],
            "action": "off",
            "description": "Apagar luces",
        }

        with patch.object(ollama_service_with_mocks, "_find_devices_by_type") as mock_find:
            mock_find.return_value = [sample_light_device]

            with patch.object(ollama_service_with_mocks, "_execute_command_on_device") as mock_exec:
                mock_exec.return_value = True

                response = ollama_service_with_mocks._generate_response(intent_analysis, user_id=1)

                assert "✓" in response or "apagado" in response

    def test_process_message_adds_to_history(self, ollama_service_with_mocks):
        """Prueba que process_message agrega a historial"""
        with (
            patch.object(ollama_service_with_mocks, "_analyze_intent") as mock_analyze,
            patch.object(ollama_service_with_mocks, "_generate_response") as mock_generate,
        ):
            mock_analyze.return_value = {
                "intent": "query",
                "device_types": [],
                "action": None,
                "description": "Test",
            }
            mock_generate.return_value = "Respuesta de prueba"

            ollama_service_with_mocks.process_message("¿Hola?", user_id=1)

            history = ollama_service_with_mocks.get_conversation_history()
            assert len(history) == 2
            assert history[0]["role"] == "user"
            assert history[0]["content"] == "¿Hola?"
            assert history[1]["role"] == "assistant"

    def test_conversation_history_persistence(self, ollama_service_with_mocks):
        """Prueba persistencia del historial en múltiples mensajes"""
        with patch.object(ollama_service_with_mocks, "_analyze_intent") as mock_analyze:
            mock_analyze.return_value = {
                "intent": "unknown",
                "device_types": [],
                "action": None,
                "description": "Test",
            }

            ollama_service_with_mocks.process_message("Pregunta 1", user_id=1)
            ollama_service_with_mocks.process_message("Pregunta 2", user_id=1)
            ollama_service_with_mocks.process_message("Pregunta 3", user_id=1)

            history = ollama_service_with_mocks.get_conversation_history()

            assert len(history) == 6  # 3 preguntas + 3 respuestas
            assert all(h["role"] in ["user", "assistant"] for h in history)

    def test_clear_history(self, ollama_service_with_mocks):
        """Prueba limpieza de historial"""
        ollama_service_with_mocks.conversation_history = [{"role": "user", "content": "test"}]

        ollama_service_with_mocks.clear_history()

        assert len(ollama_service_with_mocks.conversation_history) == 0

    def test_get_conversation_history_returns_copy(self, ollama_service_with_mocks):
        """Prueba que get_conversation_history devuelve una copia"""
        ollama_service_with_mocks.conversation_history = [{"role": "user", "content": "test"}]

        history = ollama_service_with_mocks.get_conversation_history()
        history.append({"role": "assistant", "content": "modified"})

        # La copia modificada no debe afectar el original
        assert len(ollama_service_with_mocks.conversation_history) == 1
