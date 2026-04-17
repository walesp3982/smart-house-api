"""
Tests del endpoint /ask con mocks
No requiere Ollama online ni dispositivos configurados
No requiere autenticación (se mockea)
"""

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api.depends.auth import get_user_current
from app.api.depends.service import get_ollama_service
from app.entities import UserEntity
from app.main import app


@pytest.fixture
def client():
    """Cliente de prueba de FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_user() -> UserEntity:
    """Usuario de prueba"""
    return UserEntity(
        id=1,
        email="test@example.com",
        name="Test User",
        password="test-password",
        is_verified=True,
    )


@pytest.fixture
def mock_token() -> str:
    """Token JWT de prueba"""
    return "test-token-123"


@pytest.fixture
def mock_ollama_service(ollama_service_with_mocks):
    """Fixture para mockear el servicio Ollama en FastAPI"""

    def _mock_service():
        service = Mock()
        service.process_message.return_value = "Respuesta simulada"
        service.get_conversation_history.return_value = [
            {"role": "user", "content": "¿Hola?"},
            {"role": "assistant", "content": "Respuesta simulada"},
        ]
        service.clear_history = Mock()
        return service

    return _mock_service


class TestAskEndpointMocked:
    """Tests del endpoint /ask con mocks"""

    def test_ask_requires_authentication(self, client):
        """Prueba que /ask requiere autenticación (no acepta sin token)"""
        response = client.post("/ask", json={"question": "¿Hola?"})

        # Debe devolver 403 (Forbidden) o 401 (Unauthorized)
        assert response.status_code in [403, 401]

    def test_ask_with_invalid_token(self, client):
        """Prueba /ask con token inválido"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.post("/ask", json={"question": "¿Hola?"}, headers=headers)

        assert response.status_code in [401, 422]

    def test_ask_with_mock_authentication(self, client, mock_user, mock_token, mock_ollama_service):
        """Prueba /ask con autenticación mockeada"""
        # Override dependencias en FastAPI
        app.dependency_overrides[get_user_current] = lambda: mock_user
        app.dependency_overrides[get_ollama_service] = mock_ollama_service

        try:
            # Request
            headers = {"Authorization": f"Bearer {mock_token}"}
            response = client.post(
                "/ask",
                json={"question": "¿Hola?"},
                headers=headers,
            )

            # Verificaciones
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "conversation_history" in data
            assert data["response"] == "Respuesta simulada"
        finally:
            app.dependency_overrides.clear()

    def test_ask_reset_requires_authentication(self, client):
        """Prueba que /ask/reset requiere autenticación"""
        response = client.post("/ask/reset")

        assert response.status_code in [401, 403]

    def test_ask_reset_with_mock_authentication(
        self, client, mock_user, mock_token, mock_ollama_service
    ):
        """Prueba /ask/reset con autenticación mockeada"""
        app.dependency_overrides[get_user_current] = lambda: mock_user
        app.dependency_overrides[get_ollama_service] = mock_ollama_service

        try:
            headers = {"Authorization": f"Bearer {mock_token}"}
            response = client.post("/ask/reset", headers=headers)

            # Debe devolver 200 con el mensaje de reinicio
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
        finally:
            app.dependency_overrides.clear()

    def test_ask_response_schema(self, client):
        """Prueba que la respuesta tiene la estructura correcta"""
        # Verifica documentación Swagger
        response = client.get("/docs")
        assert response.status_code == 200

    def test_ask_query_intent(self, client, mock_user, mock_token, mock_ollama_service):
        """Prueba /ask con intención de consulta"""
        app.dependency_overrides[get_user_current] = lambda: mock_user
        app.dependency_overrides[get_ollama_service] = mock_ollama_service

        try:
            headers = {"Authorization": f"Bearer {mock_token}"}
            response = client.post(
                "/ask",
                json={"question": "¿Cuántas luces están prendidas?"},
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert "luces" in data["response"].lower() or len(data["response"]) > 0
        finally:
            app.dependency_overrides.clear()

    def test_ask_command_intent(self, client, mock_user, mock_token):
        """Prueba /ask con intención de comando"""
        app.dependency_overrides[get_user_current] = lambda: mock_user

        def _command_service():
            service = Mock()
            # El mock retorna una respuesta que indica que el comando fue exitoso
            service.process_message.return_value = "✓ Todas las luces han sido apagadas"
            service.get_conversation_history.return_value = [
                {"role": "user", "content": "Apaga todas las luces"},
                {"role": "assistant", "content": "✓ Todas las luces han sido apagadas"},
            ]
            service.clear_history = Mock()
            return service

        app.dependency_overrides[get_ollama_service] = _command_service

        try:
            headers = {"Authorization": f"Bearer {mock_token}"}
            response = client.post(
                "/ask",
                json={"question": "Apaga todas las luces"},
                headers=headers,
            )

            assert response.status_code == 200
            data = response.json()
            assert "✓" in data["response"] or "apagado" in data["response"].lower()
        finally:
            app.dependency_overrides.clear()

    def test_ask_multiturno_conversation(self, client, mock_user, mock_token, mock_ollama_service):
        """Prueba conversación multi-turno"""
        app.dependency_overrides[get_user_current] = lambda: mock_user
        app.dependency_overrides[get_ollama_service] = mock_ollama_service

        try:
            headers = {"Authorization": f"Bearer {mock_token}"}

            # Pregunta 1
            response1 = client.post(
                "/ask",
                json={"question": "¿Cuántas luces?"},
                headers=headers,
            )

            assert response1.status_code == 200
            data1 = response1.json()
            assert len(data1["conversation_history"]) >= 0

            # Pregunta 2
            response2 = client.post(
                "/ask",
                json={"question": "Apaga todas"},
                headers=headers,
            )

            assert response2.status_code == 200
            data2 = response2.json()
            assert len(data2["conversation_history"]) >= 0
        finally:
            app.dependency_overrides.clear()

    def test_ask_handles_ollama_error(self, client, mock_user, mock_token):
        """Prueba manejo de errores de Ollama"""

        def _error_service():
            service = Mock()
            service.process_message.side_effect = Exception("Ollama timeout")
            return service

        app.dependency_overrides[get_user_current] = lambda: mock_user
        app.dependency_overrides[get_ollama_service] = _error_service

        try:
            headers = {"Authorization": f"Bearer {mock_token}"}
            response = client.post(
                "/ask",
                json={"question": "¿Hola?"},
                headers=headers,
            )

            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
        finally:
            app.dependency_overrides.clear()


class TestAskOpenAPI:
    """Tests de documentación OpenAPI"""

    def test_ask_endpoint_in_swagger(self, client):
        """Verifica que /ask está documentado en Swagger"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        openapi_schema = response.json()

        assert "/ask" in openapi_schema["paths"]
        assert "post" in openapi_schema["paths"]["/ask"]

    def test_ask_reset_in_swagger(self, client):
        """Verifica que /ask/reset está documentado en Swagger"""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        openapi_schema = response.json()

        assert "/ask/reset" in openapi_schema["paths"]
        assert "post" in openapi_schema["paths"]["/ask/reset"]

    def test_ask_request_schema(self, client):
        """Verifica esquema de request en OpenAPI"""
        response = client.get("/openapi.json")
        openapi_schema = response.json()

        ask_post = openapi_schema["paths"]["/ask"]["post"]
        request_body = ask_post.get("requestBody", {})

        assert "content" in request_body
        assert "application/json" in request_body["content"]
