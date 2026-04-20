# 🧪 Tests para Ollama - Smart House API

## 📋 Descripción

Tests para la integración de Ollama con la API:

- **`test_ollama_service.py`**: Tests unitarios (NO requiere Ollama)
- **`test_ollama_integration.py`**: Tests de integración (REQUIERE Ollama online)
- **`test_ask_endpoint.py`**: Tests del endpoint `/ask` (NO requiere Ollama)
- **`conftest_ollama.py`**: Fixtures compartidas para todos los tests

---

## 🚀 Instalación de Dependencias

```bash
pip install pytest pytest-mock pytest-asyncio
```

---

## ▶️ Ejecutar Tests

### **1️⃣ Tests Unitarios (SIN Ollama)**
Sin necesidad de Ollama corriendo:

```bash
# Ejecutar todos los tests unitarios
pytest tests/test_ollama_service.py -v

# Con output detallado
pytest tests/test_ollama_service.py -v -s

# Tests específicos
pytest tests/test_ollama_service.py::TestOllamaServiceWithoutServer::test_call_ollama_mocked -v
```

### **2️⃣ Tests del Endpoint (SIN Ollama)**
Sin necesidad de Ollama corriendo:

```bash
# Ejecutar todos los tests del endpoint
pytest tests/test_ask_endpoint.py -v

# Solo tests que requieren autenticación mockeada
pytest tests/test_ask_endpoint.py::TestAskEndpointMocked -v
```

### **3️⃣ Tests de Integración (CON Ollama)**
REQUIERE que Ollama esté corriendo:

```bash
# Primero, asegúrate de que Ollama esté corriendo
ollama serve

# En otra terminal
pytest tests/test_ollama_integration.py -v

# Si Ollama no está disponible, los tests se saltan automáticamente
```

### **4️⃣ Ejecutar TODOS los tests**

```bash
# Tests unitarios + endpoint + integración
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html

# Solo tests que no requieren Ollama
pytest tests/test_ollama_service.py tests/test_ask_endpoint.py -v
```

---

## 🏗️ Estructura de Tests

### **Test Unitarios** (`test_ollama_service.py`)
✅ NO requiere Ollama online
✅ Rápidos (< 1 segundo)
✅ Usa mocks para todos los servicios
✅ 20+ casos de prueba

```python
# Ejemplo
def test_call_ollama_mocked(self, ollama_service_with_mocks):
    with patch("app.services.ollama.subprocess.run") as mock_run:
        mock_run.return_value.stdout = "Respuesta simulada"
        result = ollama_service_with_mocks._call_ollama("¿Hola?")
        assert "simulada" in result
```

---

### **Tests de Integración** (`test_ollama_integration.py`)
⚠️ REQUIERE Ollama online (`ollama serve`)
🐢 Lentos (5-30 segundos por test)
✅ Prueba con Ollama real
✅ Se saltan automáticamente si Ollama no está disponible

```python
# Ejemplo
def test_call_ollama_real(self, ollama_service_with_mocks):
    response = ollama_service_with_mocks._call_ollama(
        "¿Cuántos días tiene una semana?"
    )
    assert "Error" not in response
```

---

### **Tests del Endpoint** (`test_ask_endpoint.py`)
✅ NO requiere Ollama online
✅ Prueba endpoint FastAPI
✅ Mockea autenticación JWT
✅ Verifica esquema OpenAPI

```python
# Ejemplo
@patch("app.api.depends.auth.get_user_current")
def test_ask_with_mock_authentication(self, mock_get_user, client):
    mock_get_user.return_value = mock_user
    response = client.post("/ask", json={"question": "¿Hola?"})
    assert response.status_code == 200
```

---

## 📊 Casos de Prueba Incluidos

### Unitarios (20 tests)
- [ ] `_call_ollama()` con mock
- [ ] Timeout en Ollama
- [ ] Ollama no instalado
- [ ] Dispositivos vacíos
- [ ] Dispositivos con estado
- [ ] Análisis de intención (query)
- [ ] Análisis de intención (command)
- [ ] JSON inválido
- [ ] Búsqueda por tipo
- [ ] Ejecución de comandos
- [ ] Comandos inválidos
- [ ] Respuestas sin dispositivos
- [ ] Respuestas con comandos ejecutados
- [ ] Historial de conversación
- [ ] Múltiples mensajes
- [ ] Limpieza de historial
- [ ] Copia de historial

### Integración (6 tests)
- [ ] Llamada real a Ollama
- [ ] Timeout en llamada real
- [ ] Análisis real (query)
- [ ] Análisis real (command)
- [ ] Procesamiento completo
- [ ] Manejo offline

### Endpoint (12 tests)
- [ ] Autenticación requerida
- [ ] Token inválido
- [ ] Autenticación mockeada
- [ ] Reset requiere autenticación
- [ ] Schema de respuesta
- [ ] Intent tipo query
- [ ] Intent tipo command
- [ ] Conversación multi-turno
- [ ] Manejo de errores
- [ ] Swagger documentation
- [ ] Reset endpoint
- [ ] OpenAPI schema

---

## 🔍 Ejemplos de Ejecución

### **Ejemplo 1: Ejecutar un test específico**
```bash
pytest tests/test_ollama_service.py::TestOllamaServiceWithoutServer::test_analyze_intent_query -v
```

### **Ejemplo 2: Ejecutar con output detallado**
```bash
pytest tests/test_ollama_service.py -v -s --tb=short
```

### **Ejemplo 3: Ejecutar y generar reporte HTML**
```bash
pytest tests/ --cov=app --cov-report=html
# Abre htmlcov/index.html en el navegador
```

### **Ejemplo 4: Ejecutar solo tests rápidos (sin integración)**
```bash
pytest tests/test_ollama_service.py tests/test_ask_endpoint.py -v --maxfail=3
```

### **Ejemplo 5: Watch mode (re-ejecutar cuando cambia código)**
```bash
pytest-watch tests/ -c
```

---

## ⚙️ Configuración

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Fixtures Disponibles

| Fixture | Descripción |
|---------|-------------|
| `mock_installed_device_service` | Mock del servicio de dispositivos |
| `mock_state_device_service` | Mock del servicio de estado |
| `mock_command_device_service` | Mock del servicio de comandos |
| `mock_track_device_service` | Mock del servicio de tracking |
| `mock_mqtt_provider` | Mock del proveedor MQTT |
| `ollama_service_with_mocks` | OllamaConversationService configurado |
| `sample_light_device` | Dispositivo luz de prueba |
| `sample_door_device` | Dispositivo puerta de prueba |
| `client` | Cliente FastAPI para tests |
| `mock_user` | Usuario de prueba |
| `mock_token` | Token JWT de prueba |

---

## 🐛 Troubleshooting

### **Error: "Ollama no está disponible"**
```bash
# En otra terminal
ollama serve

# El test debería ejecutarse sin problemas
pytest tests/test_ollama_integration.py -v
```

### **Error: "ModuleNotFoundError: No module named 'app'"**
```bash
# Asegúrate de estar en la raíz del proyecto
cd /proyectos/smart-house-api

# Y que el PYTHONPATH incluya src/
export PYTHONPATH="${PYTHONPATH}:./src"

pytest tests/ -v
```

### **Error: "fixtures not found"**
```bash
# Verifica que conftest_ollama.py tenga las fixtures
# O cámbiale el nombre a conftest.py

mv tests/conftest_ollama.py tests/conftest.py
pytest tests/ -v
```

---

## 📈 Cobertura de Código

```bash
# Ejecutar con cobertura
pytest tests/ --cov=app/services/ollama --cov-report=term-missing

# Generar reporte HTML
pytest tests/ --cov=app --cov-report=html

# Ver reporte
open htmlcov/index.html
```

---

## 🎯 Próximas Mejoras

- [ ] Tests de load/stress
- [ ] Tests de concurrencia
- [ ] Fixtures para diferentes modelos de Ollama
- [ ] Tests de fallback a otros modelos
- [ ] Screenshots en Allure reports

---

**¡Todos los tests están listos para ejecutar! 🚀**
