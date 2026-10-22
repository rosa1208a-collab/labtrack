"""Comprobación sin instalar, modificar ni imprimir secretos."""

import argparse
import shutil
import socket
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--docker", action="store_true")
args = parser.parse_args()
failures = []


def check(label, valid):
    print(f"{'OK' if valid else 'REVISAR'}: {label}")
    if not valid:
        failures.append(label)


check("Python 3.11 o superior", sys.version_info >= (3, 11))
check("Git instalado", shutil.which("git") is not None)
for key in ["user.name", "user.email"]:
    if shutil.which("git"):
        result = subprocess.run(["git", "config", "--get", key], capture_output=True)
        check(f"Git tiene {key}", result.returncode == 0 and bool(result.stdout.strip()))
with socket.socket() as sock:
    try:
        sock.bind(("127.0.0.1", 8010))
        check("Puerto 8010 disponible", True)
    except OSError:
        check("Puerto 8010 disponible (o LabTrack ya está ejecutándose)", False)
if args.docker:
    if shutil.which("docker"):
        for command in [["docker", "info"], ["docker", "compose", "version"]]:
            try:
                result = subprocess.run(command, capture_output=True, timeout=20)
                check(" ".join(command), result.returncode == 0)
            except subprocess.TimeoutExpired:
                check(" ".join(command), False)
    else:
        check("Docker instalado", False)
print("Comprueba también conexión a Internet y acceso a tu agente de IA.")
sys.exit(bool(failures))
