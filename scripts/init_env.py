"""Genera secretos locales sin reemplazar una configuración existente."""

import secrets
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / ".env"
if target.exists():
    print(".env ya existe; se conserva sin cambios.")
else:
    content = (root / ".env.example").read_text(encoding="utf-8")
    content = content.replace(
        "POSTGRES_PASSWORD=GENERAR_CON_INIT_ENV", f"POSTGRES_PASSWORD={secrets.token_urlsafe(30)}"
    )
    content = content.replace(
        "DEMO_PASSWORD=GENERAR_CON_INIT_ENV", f"DEMO_PASSWORD={secrets.token_urlsafe(18)}"
    )
    with target.open("x", encoding="utf-8") as stream:
        stream.write(content)
    target.chmod(0o600)
    print(".env creado. Consulta DEMO_PASSWORD en tu editor para entrar a la demo.")
