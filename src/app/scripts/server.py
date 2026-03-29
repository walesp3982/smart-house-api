import subprocess


def dev():
    try:
        subprocess.run(["fastapi", "dev", "src/app/main.py"])
    except KeyboardInterrupt:
        pass


def prod():
    try:
        subprocess.run(["fastapi", "run", "src/app/main.py", "--host", "0.0.0.0"])
    except KeyboardInterrupt:
        pass
