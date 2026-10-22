"""Exporta puntos de recuperación independientes; no copia secretos ni datos."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
DIRECTORIES = {"app", "frontend", "migrations", "tests", "scripts", "docs", "prompts", ".github"}
FILES = {
    "README.md",
    "AGENTS.md",
    ".gitignore",
    ".dockerignore",
    ".env.example",
    "pyproject.toml",
    "alembic.ini",
    "requirements.txt",
    "requirements-dev.txt",
    "Dockerfile",
    "compose.yaml",
}
STAGES = {
    "00-inicio": (
        "Autenticación e interfaz listas. Implementa proyectos y experimentos.",
        {"projects", "experiments"},
    ),
    "01-proyectos": (
        "CRUD de proyectos resuelto. Implementa experimentos y sus permisos.",
        {"experiments"},
    ),
    "02-completo": ("Solución de referencia: CRUD, permisos, filtros, resumen y Docker.", set()),
}


def placeholder(module):
    paths = (
        ["/projects", "/projects/{project_id}"]
        if module == "projects"
        else ["/projects/{project_id}/experiments", "/experiments/{experiment_id}"]
    )
    decorators = "\n".join(
        f'@router.api_route("{path}", methods=["GET", "POST", "PUT", "DELETE"])' for path in paths
    )
    return (
        '"""Ejercicio: implementa el contrato de docs/02-arquitectura.md."""\n'
        "from fastapi import APIRouter, Depends, HTTPException\n"
        "from app.security import get_current_user\n\n"
        f'router = APIRouter(tags=["{module}"], dependencies=[Depends(get_current_user)])\n\n'
        f"{decorators}\ndef pending():\n"
        "    raise HTTPException(501, "
        f'"Etapa pendiente: implementa {module} con el prompt correspondiente.")\n'
    )


def main():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    selected = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(
            part in {"__pycache__", ".pytest_cache", ".ruff_cache"} for part in rel.parts
        ):
            continue
        if rel.parts[0] in DIRECTORIES or str(rel) in FILES:
            selected.append((path, rel.as_posix()))
    for stage, (description, missing) in STAGES.items():
        target = output / f"labtrack-{stage}.zip"
        with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
            prefix = f"labtrack-{stage}/"
            for path, rel in selected:
                module = Path(rel).stem
                if rel.startswith("app/routes/") and module in missing:
                    content = placeholder(module).encode()
                else:
                    content = path.read_bytes()
                archive.writestr(prefix + rel, content)
            archive.writestr(
                prefix + "ETAPA.md",
                f"# {stage}\n\n{description}\n\n"
                "Sigue README.md y docs/03-ruta-basica.md o docs/04-ruta-avanzada.md.\n\n"
                "Los endpoints pendientes responden 501 de forma intencional. "
                "En 00-inicio y 01-proyectos ejecuta primero tests/test_auth.py; "
                "las pruebas de dominio describen el objetivo y fallarán "
                "hasta implementar el CRUD. "
                "En 02-completo debe pasar toda la suite.\n\n"
                "Conserva tu carpeta anterior; extrae cada recuperación en una carpeta nueva.\n",
            )
        print(target.name)


if __name__ == "__main__":
    main()
