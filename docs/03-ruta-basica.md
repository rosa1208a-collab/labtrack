# Ruta básica · Python y SQLite

## Antes de comenzar

Necesitas Python 3.11 o superior, VS Code, Git y una herramienta de IA a la que puedas acceder. Recomendamos Python 3.12. Las cuotas de los agentes dependen de tu cuenta; conserva los puntos de recuperación para continuar si se agota una cuota. Esta ruta no necesita Docker ni Node.js.

Extrae `labtrack-00-inicio.zip` en una carpeta propia y ábrela en VS Code. Si trabajas con la solución completa, abre la carpeta que contiene `alembic.ini`. No instales las dependencias de `grades_ai`: LabTrack tiene las suyas.

## 1. Crear el entorno

macOS/Linux:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

Si `python3` corresponde a una versión anterior a 3.11, usa el ejecutable de la versión instalada, por ejemplo `python3.12`, en los dos primeros comandos.

Windows PowerShell:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si tienes 3.11, sustituye `-3.12` por `-3.11`. Si PowerShell bloquea la activación, no necesitas cambiar políticas del equipo: ejecuta los comandos siguientes usando `.\.venv\Scripts\python.exe` en lugar de `python`.

## 2. Preparar la aplicación

Desde el entorno virtual:

```bash
python scripts/check_environment.py
python -m pip install -r requirements-dev.txt
python scripts/init_env.py
python -m alembic upgrade head
python -m app.cli seed-demo
```

`init_env.py` crea `.env` con contraseñas aleatorias y nunca reemplaza uno existente. Abre `.env` en el editor y localiza `DEMO_PASSWORD`. Es la contraseña local para `ana@example.com` y `luis@example.com`. No compartas ese archivo ni lo subas a GitHub.

`seed-demo` crea dos cuentas con proyectos y experimentos ficticios. Ejecutarlo nuevamente conserva los datos y las contraseñas existentes.

## 3. Arrancar

```bash
python -m uvicorn app.main:create_app --factory --reload --host 127.0.0.1 --port 8010
```

Abre http://127.0.0.1:8010 e inicia sesión. La terminal debe permanecer abierta. Detén el servidor con Ctrl+C. El archivo de datos se guarda en `data/labtrack.db`.

En `00-inicio` los endpoints de proyectos y experimentos responden **501** intencionalmente. El acceso funciona y la interfaz indica qué módulo falta. En `01-proyectos` solo faltan experimentos. En `02-completo` funciona todo.

## 4. Construir por etapas

1. Lee los requisitos y el ERD. Usa los prompts 01 y 02 para entenderlos.
2. Copia el contexto común del prompt 00 al agente.
3. Usa el prompt 03 para implementar proyectos: crear, consultar, editar y eliminar.
4. Prueba el primer proyecto con tu navegador. Observa su petición en la pestaña Red/Network.
5. Usa el prompt 04 para experimentos, filtros y permisos.
6. Usa el prompt 05 para comprobar el resultado y depurar.

No pidas al agente que reemplace la plantilla completa. Conserva autenticación, validadores y migraciones. Al comenzar, el esquema de BD ya existe: el ejercicio principal consiste en conectar la lógica del dominio y la interfaz.

## 5. Comprobar

En otra terminal con el mismo entorno activo:

```bash
python -m pytest tests/test_auth.py -q
python -m pytest tests/test_domain.py -q
python -m pytest tests/test_migrations.py -q
python -m ruff check .
```

Las pruebas usan bases temporales; no borran tu archivo de datos. La primera suite debe pasar desde el inicio. La de dominio se completa al implementar el CRUD. Con la solución terminada ejecuta `python -m pytest -q`.

Prueba manual: crea un proyecto, detén el servidor, vuelve a arrancarlo y comprueba que existe. Entra como Luis en una ventana privada y verifica que no aparece. La suite comprueba además intentos de acceso directo a los IDs ajenos.

## Entrega básica

- Aplicación ejecutable con acceso, proyectos y experimentos.
- Evidencia del CRUD y persistencia tras reiniciar.
- Pruebas de permisos y validación pasando.
- README con los comandos de arranque y prueba.
- Diagrama de arquitectura y ERD que correspondan al código.
- Una explicación de qué ocurre al pulsar Guardar.

Para recuperar una etapa, extrae su ZIP en una carpeta nueva. Conserva tu trabajo anterior. No sobrescribas una carpeta con cambios ni copies contraseñas al material que entregues.
