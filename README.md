# smart-house-api
## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto en tu entorno local:

### 1. Clona el repositorio

```bash
git clone https://github.com/walesp3982/smart-house-api.git
cd smart-house-api
```

### 2. Crea y activa un entorno virtual (opcional pero recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

Si aún no tienes `uv` instalado, puedes hacerlo desde [aquí](https://docs.astral.sh/uv/).

```bash
uv add -r requirements.txt
```

### 4. Ejecuta la aplicación

```bash
cd app
python main.py
```

---
Si tienes dudas o problemas, revisa la documentación o abre un issue.
Es la api para la casa inteligente
