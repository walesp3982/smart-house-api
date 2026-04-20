# 🏠 Smart House API - Sistema de Preguntas con Ollama

## ✅ Estado: Sistema Implementado y Funcionando

El servidor FastAPI está corriendo en **http://localhost:8000** con soporte para preguntas/órdenes con Ollama.

---

## 🚀 Cómo Usar

### 1. **Asegúrate de que Ollama está corriendo**

```bash
# En otra terminal/ventana
ollama serve

# O simplemente verifica que llama2 está descargado
ollama list
```

### 2. **El servidor está en:**
```
http://localhost:8000
```

### 3. **Documentación interactiva:**
```
http://localhost:8000/docs
```

---

## 💬 Ejemplos de Uso

### **Ejemplo 1: Consultar estado de dispositivos**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuántas luces están prendidas?"
  }'
```

**Respuesta:**
```json
{
  "response": "Tienes 2 luces encendidas en la sala y la cocina",
  "conversation_history": [...]
}
```

---

### **Ejemplo 2: Dar una orden**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Apaga todas las luces"
  }'
```

**Respuesta:**
```json
{
  "response": "✓ He apagado correctamente: Luz sala, Luz cocina",
  "conversation_history": [...]
}
```

---

### **Ejemplo 3: Preguntar por temperatura**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es la temperatura actual?"
  }'
```

---

### **Ejemplo 4: Reiniciar conversación**

```bash
curl -X POST http://localhost:8000/ask/reset \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📋 Preguntas Soportadas

| Tipo | Ejemplos |
|------|----------|
| **Estado de luces** | "¿Cuántas luces están prendidas?", "¿Está encendida la luz de la sala?" |
| **Apagar dispositivos** | "Apaga todas las luces", "Apaga la puerta", "Apaga los sensores" |
| **Encender dispositivos** | "Enciende la luz", "Abre la cámara", "Enciende el aire" |
| **Temperatura** | "¿Cuál es la temperatura?", "¿Qué temperatura hace?" |
| **Múltiples dispositivos** | "¿Cuál es el estado de todo?", "Apaga todo" |

---

## 🔐 Requisitos

1. ✅ **Ollama instalado** (ya está)
2. ✅ **Modelo llama2 descargado** (ya está)
3. ✅ **FastAPI corriendo** (ya está en :8000)
4. 📝 **Token JWT válido** (necesitas estar autenticado)
5. 🏠 **Dispositivos instalados** (en tu casa inteligente)

---

## 🔄 Flujo del Sistema

```
Usuario pregunta
    ↓
Ollama analiza la intención (query o command)
    ↓
Sistema consulta estado real MQTT (si es query)
O ejecuta comando en dispositivo (si es command)
    ↓
Respuesta en lenguaje natural
    ↓
Historial guardado en sesión
```

---

## 📝 Notas Importantes

### Tiempo de Respuesta
- **Primera pregunta**: 10-30 segundos (Ollama carga el modelo)
- **Preguntas siguientes**: 5-15 segundos

### Límites
- La sesión mantiene **SO LO UN USUARIO**
- El historial se limpia al reiniciar el servidor
- Máximo timeout: 30 segundos por pregunta

### MQTT
- El sistema se conecta automáticamente a tu broker MQTT
- Los comandos se publican en topics: `/{device_uuid}/action`
- Los estados se leen desde: `/{device_uuid}/value`

---

## 🐛 Si Algo No Funciona

### Ollama no responde
```bash
# Verifica que Ollama está corriendo
ollama serve

# En otra terminal
ollama run llama2 "Hola"
```

### Error 401 (Token inválido)
- Necesitas un token JWT válido
- Haz login primero: `POST /auth/login`
- Usa el token en el header: `Authorization: Bearer {token}`

### Error 500 (Error interno)
```bash
# Revisa los logs del servidor
# En la terminal de uvicorn verás los errores
```

---

## 🎯 Archivos Creados/Modificados

```
✅ src/app/services/ollama.py           → Servicio principal
✅ src/app/main.py                      → Rutas /ask y /ask/reset
✅ src/app/api/depends/service.py       → Inyección de dependencias
✅ OLLAMA_GUIDE.md                      → Documentación completa
✅ test_ollama_ask.py                   → Script de prueba
```

---

## 📚 Documentación Completa

Ver [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md) para más detalles técnicos.

---

## ✨ Características Implementadas

- ✅ Análisis inteligente de intención (query vs command)
- ✅ Contexto de conversación multi-turno
- ✅ Consulta de estado real vía MQTT
- ✅ Ejecución de comandos automática
- ✅ Respuestas en lenguaje natural
- ✅ Historial de conversación
- ✅ Soporte multiidioma (español/inglés)

---

## 🎓 Ejemplo Completo Python

```python
import requests

# Credenciales
TOKEN = "tu_token_aqui"
BASE_URL = "http://localhost:8000"

# Headers
headers = {"Authorization": f"Bearer {TOKEN}"}

# Preguntas
questions = [
    "¿Cuántas luces están prendidas?",
    "Apaga todas las luces",
    "¿Cuál es la temperatura?"
]

for q in questions:
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"question": q},
        headers=headers
    )
    
    data = response.json()
    print(f"💬 Pregunta: {q}")
    print(f"🤖 Respuesta: {data['response']}\n")
```

---

**¡El sistema está listo! 🚀**

Ahora puedes hacer preguntas al azar y Ollama responderá automáticamente.
