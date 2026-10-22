# LabTrack · Del prompt al despliegue

Proyecto y material del taller de desarrollo de software con agentes de IA. Una bitácora de proyectos y experimentos con frontend, API, autenticación y base de datos.

**Esta carpeta contiene la solución completa de referencia.** Para empezar el ejercicio, el docente distribuye `labtrack-00-inicio.zip`. Si recibiste un ZIP, lee también `ETAPA.md`.

## Empieza aquí

1. Lee [la guía del taller](docs/01-taller.md).
2. Elige [ruta básica: Python + SQLite](docs/03-ruta-basica.md) o [ruta avanzada: Docker + PostgreSQL](docs/04-ruta-avanzada.md).
3. Consulta [requisitos, arquitectura, ERD y API](docs/02-arquitectura.md).
4. Copia los [prompts por etapa](prompts/README.md), uno por vez.
5. Comprueba la entrega con [ejercicios y rúbrica](docs/06-ejercicios-evaluacion.md).

Docentes: [guion de cuatro horas](docs/05-guia-docente.md), [resolución de problemas](docs/07-problemas-frecuentes.md) y [despliegue en un servidor](docs/08-despliegue.md).

## Arranque rápido de la solución completa

Abre una terminal **en esta carpeta**, donde están `alembic.ini` y `compose.yaml`. Usa Python 3.11 o superior; recomendamos 3.12. Estos comandos presuponen el entorno virtual activado; la guía básica explica la activación en cada sistema.

```bash
python -m pip install -r requirements-dev.txt
python scripts/init_env.py
python -m alembic upgrade head
python -m app.cli seed-demo
python -m uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8010
```

Abre http://127.0.0.1:8010. Usuarios de ejemplo: `ana@example.com` y `luis@example.com`. La contraseña aleatoria se genera en el campo `DEMO_PASSWORD` del archivo local `.env`. No existe una contraseña compartida dentro del código.

Alternativa con Docker, después de generar `.env`:

```bash
docker compose up -d --build --wait
docker compose exec app python -m app.cli seed-demo
```

## Qué incluye

- Frontend en español con formularios, estados vacíos, mensajes y diseño adaptable.
- FastAPI con documentación interactiva en `/docs` y estado en `/health`.
- Contraseñas Argon2, sesiones revocables almacenadas en la BD y cookies HttpOnly.
- Validación de origen y token CSRF para operaciones autenticadas que modifican datos.
- CRUD de proyectos y experimentos; aislamiento por propietario.
- Filtro exacto por modelo, resumen real y restricción al eliminar proyectos con experimentos.
- SQLAlchemy, migraciones Alembic, SQLite y PostgreSQL.
- Docker Compose con persistencia, healthchecks, migraciones y contenedor sin privilegios.
- Pruebas automáticas y workflow de GitHub Actions para un repositorio independiente.

## Comprobar

```bash
python -m pytest -q
python -m ruff check .
```

Pruebas en Docker, con bases SQLite y PostgreSQL de prueba aisladas:

```bash
docker compose --profile test run --build --rm tests
docker compose --profile test stop test-db
```

En las etapas incompletas empieza con `python -m pytest tests/test_auth.py -q`. Las pruebas de dominio describen el objetivo y fallan intencionalmente hasta completar el ejercicio.

## Preparar paquetes para el grupo

```bash
python scripts/package_workshop.py
```

Produce tres ZIP en `dist/`: `00-inicio`, `01-proyectos` y `02-completo`. No incluyen `.env`, bases de datos, entornos virtuales ni contraseñas. Cada participante genera su propia configuración.

## Convertirlo en repositorio propio

Copia el contenido de un ZIP a una carpeta nueva y crea ahí tu repositorio de GitHub. La carpeta `.github/workflows` debe estar en la raíz de ese repositorio para que CI se ejecute. Dentro del monorepositorio `grades_ai` es solo una plantilla y no modifica sus workflows ni su aplicación.

Los commits y la publicación los realiza el participante o el docente. El material no presupone una URL de GitHub ya creada. Nunca subas `.env`, `data/` o `.venv/`.

## Alcance

MVP educativo desplegable. No entrena modelos, ejecuta notebooks ni sube archivos. Los resultados demo son sintéticos. El despliegue local está limitado a `127.0.0.1`; la publicación con HTTPS se explica como una etapa adicional. No se ha contratado ni configurado hosting externo.
