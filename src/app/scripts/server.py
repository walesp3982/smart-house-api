import subprocess


def dev():
    try:
        subprocess.run(["fastapi", "dev", "src/app/main.py", "--host", "0.0.0.0"])
    except KeyboardInterrupt:
        pass


def prod():
    try:
        subprocess.run(["fastapi", "run", "src/app/main.py", "--host", "0.0.0.0"])
    except KeyboardInterrupt:
        pass


def uvicorn_dev():
    try:
        subprocess.run(["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        pass
