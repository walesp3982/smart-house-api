import subprocess


def dev():
    subprocess.run(["fastapi", "dev", "src/app/main.py"])


def prod():
    subprocess.run(["fastapi", "run", "src/app/main.py", "--host", "0.0.0.0"])
