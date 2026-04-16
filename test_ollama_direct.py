#!/usr/bin/env python3
"""
Script simple para probar que Ollama responde correctamente
Sin necesidad de token JWT
"""

import json
import subprocess


def test_ollama_directly():
    """
    Prueba Ollama directamente sin pasar por la API
    """
    print("=" * 70)
    print("PRUEBA DIRECTA DE OLLAMA")
    print("=" * 70)

    # Verifica que Ollama esté corriendo
    print("\n🔍 Verificando que Ollama está corriendo...")
    try:
        result = subprocess.run(
            ["ollama", "--version"], capture_output=True, text=True, timeout=5
        )
        print(f"✓ Ollama instalado: {result.stdout.strip()}")
    except FileNotFoundError:
        print("✗ Ollama no está instalado o no está en PATH")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Ollama tardó mucho en responder")
        return False

    # Prueba preguntas simples
    print("\n" + "-" * 70)
    print("PRUEBAS DE PREGUNTAS")
    print("-" * 70)

    test_questions = [
        "¿Cuántos dispositivos de luz puede haber en una casa?",
        "¿Qué es una casa inteligente?",
        "¿Cómo se apagan las luces automáticamente?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n📤 Pregunta {i}: {question}")
        print("   Esperando respuesta de Ollama (puede tomar 10-30 segundos)...")

        try:
            result = subprocess.run(
                ["ollama", "run", "llama2", question],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                response = result.stdout.strip()
                # Truncar respuesta larga
                if len(response) > 200:
                    response = response[:200] + "..."
                print(f"   ✓ Respuesta: {response}")
            else:
                print(f"   ✗ Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("   ✗ Timeout: Ollama tardó mucho en responder")
        except Exception as e:
            print(f"   ✗ Error: {e}")

    # Prueba análisis JSON
    print("\n" + "-" * 70)
    print("PRUEBA DE ANÁLISIS JSON (simulando intención)")
    print("-" * 70)

    json_prompt = """Responde SOLO con un JSON válido sin explicaciones adicionales.
    {
        "intent": "query" o "command",
        "device_types": ["light", "door", "camera", "movement", "temperature"],
        "action": "on" o "off" o null,
        "description": "breve descripción"
    }
    
    Analiza: "Apaga todas las luces"
    """

    print("\n📤 Intentando que Ollama devuelva JSON...")
    try:
        result = subprocess.run(
            ["ollama", "run", "llama2", json_prompt],
            capture_output=True,
            text=True,
            timeout=60,
        )

        response = result.stdout.strip()
        print(f"   Respuesta de Ollama:\n   {response[:300]}")

        # Intenta parsear JSON
        if "{" in response and "}" in response:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]

            try:
                parsed = json.loads(json_str)
                print(f"\n   ✓ JSON válido detectado:")
                print(f"   {json.dumps(parsed, indent=4, ensure_ascii=False)}")
            except json.JSONDecodeError as e:
                print(f"   ✗ JSON inválido: {e}")
        else:
            print("   ⚠ No se encontró JSON en la respuesta")

    except subprocess.TimeoutExpired:
        print("   ✗ Timeout")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n" + "=" * 70)
    print("PRUEBA COMPLETADA")
    print("=" * 70)
    print(
        "\n💡 Si Ollama responde correctamente, el sistema /ask funcionará sin problemas"
    )
    print("   Próximo paso: Executar test_ollama_ask.py con un usuario registrado")

    return True


if __name__ == "__main__":
    test_ollama_directly()
