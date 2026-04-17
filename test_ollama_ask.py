#!/usr/bin/env python3
"""
Script de prueba para la ruta /ask con Ollama
Verifica que el sistema responda preguntas correctamente
"""

import sys

import requests

# URLs de la API
BASE_URL = "http://localhost:8000"
AUTH_ENDPOINT = f"{BASE_URL}/auth/login"
ASK_ENDPOINT = f"{BASE_URL}/ask"


def test_ask_endpoint():
    """
    Prueba la ruta /ask sin autenticación primero
    Luego con autenticación
    """
    print("=" * 60)
    print("PRUEBA DE RUTA /ask CON OLLAMA")
    print("=" * 60)

    # Primero verificamos que el servidor está corriendo
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Servidor está corriendo: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("✗ El servidor no está corriendo en http://localhost:8000")
        print("  Inicia con: python -m uvicorn src.app.main:app --reload")
        return False

    print("\n" + "-" * 60)
    print("NOTA: Para probar la ruta /ask necesitas:")
    print("1. Un usuario registrado")
    print("2. Un token JWT válido")
    print("3. Dispositivos instalados en la casa")
    print("-" * 60)

    # Intenta hacer login con credenciales de prueba
    test_credentials = {"email": "user@example.com", "password": "password123"}

    print("\n📝 Intentando login con credenciales de prueba...")
    print(f"   Email: {test_credentials['email']}")

    try:
        auth_response = requests.post(AUTH_ENDPOINT, json=test_credentials)

        if auth_response.status_code == 200:
            token_data = auth_response.json()
            token = token_data.get("access_token")
            print(f"✓ Login exitoso! Token: {token[:20]}...")

            # Ahora prueba /ask con el token
            print("\n🔊 Haciendo pregunta a Ollama...")

            questions = [
                "¿Cuántas luces están prendidas?",
                "¿Cuál es el estado de los dispositivos?",
                "Apaga todas las luces",
            ]

            headers = {"Authorization": f"Bearer {token}"}

            for question in questions:
                print(f"\n📤 Pregunta: {question}")
                ask_response = requests.post(
                    ASK_ENDPOINT, json={"question": question}, headers=headers
                )

                if ask_response.status_code == 200:
                    response_data = ask_response.json()
                    print(f"📥 Respuesta: {response_data['response']}")
                    print(f"   Historial: {len(response_data['conversation_history'])} mensajes")
                else:
                    print(f"✗ Error {ask_response.status_code}: {ask_response.text}")
        else:
            print(f"✗ Login fallido: {auth_response.status_code}")
            print(f"   {auth_response.text}")
            print("\n💡 Sugerencia: Necesitas crear un usuario primero")
            print("   POST /auth/register")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error en la solicitud: {e}")
        return False

    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_ask_endpoint()
    sys.exit(0 if success else 1)
