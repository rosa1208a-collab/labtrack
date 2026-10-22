# Ruta avanzada · Docker Compose y PostgreSQL

## Requisitos adicionales

Docker con Compose funcionando y capacidad para descargar imágenes y dependencias. En Windows, completa previamente la instalación del motor y la virtualización requerida por tu distribución. No dejes esa instalación para los primeros quince minutos. Reserva espacio adicional para imágenes: los 5 GB del cartel no garantizan espacio suficiente para un entorno Docker completo.

Trabaja en la carpeta que contiene `compose.yaml`. Necesitas Python 3.11+ para los scripts de preparación del taller; la aplicación se ejecutará con Python 3.12 dentro del contenedor.

## 1. Preparar y arrancar

En macOS/Linux usa `python3` o el ejecutable Python 3.11+ instalado; en Windows usa `py -3.12` o `py -3.11`.

```bash
python3 scripts/check_environment.py --docker
python3 scripts/init_env.py
docker compose config --quiet
docker compose up -d --build --wait
docker compose exec app python -m app.cli seed-demo
docker compose ps
```

Abre http://127.0.0.1:8010. Usa las cuentas ficticias `ana@example.com` y `luis@example.com` con el valor `DEMO_PASSWORD` de tu `.env`.

No ejecutes al mismo tiempo el servidor básico en el puerto 8010. Detén uno antes de iniciar el otro. SQLite y PostgreSQL son bases diferentes: cambiar de ruta no copia automáticamente los datos.

## 2. Entender los servicios

- `db`: PostgreSQL, accesible dentro de la red de Compose. Su volumen conserva los datos.
- `migrate`: aplica `alembic upgrade head` cuando la BD está disponible y termina con código 0.
- `app`: entrega la interfaz y la API después de migrar; corre como usuario sin privilegios.
- Perfil `test`: añade `test-db` y `tests` para probar con SQLite y PostgreSQL sin tocar la BD de la aplicación.

El nombre `db` funciona entre servicios. `localhost` dentro de un contenedor se refiere a ese mismo contenedor. El navegador usa `127.0.0.1:8010`; la aplicación usa `db:5432`.

Los valores de `.env` configuran Compose. La URL PostgreSQL se inyecta en el contenedor; el valor SQLite de `DATABASE_URL` se utiliza al ejecutar Python directamente en tu equipo.

## 3. Desarrollar y consultar logs

```bash
docker compose logs --tail=100 app migrate db
docker compose up -d --build --wait
docker compose exec app alembic current
```

No se montan carpetas de código ni se activa `--reload` en el contenedor. Después de editar, reconstruye la imagen. El punto inicial trae la infraestructura para evitar bloqueos; usa el prompt 06 para explicarla, comprobarla y practicar cambios en una copia.

## 4. Probar ambos motores

```bash
docker compose --profile test run --build --rm tests
docker compose --profile test stop test-db
```

La suite ejecuta cada caso con SQLite y PostgreSQL. `test-db` usa una base llamada `labtrack_test`, sin puerto publicado y sin volumen persistente. La contraseña visible en ese servicio es exclusivamente para pruebas aisladas y no se reutiliza en la app.

Las fixtures eliminan tablas de la BD de prueba; solo aceptan un nombre terminado en `_test`. Nunca apuntes `TEST_DATABASE_URL` a la BD de la aplicación.

## 5. Comprobar persistencia de verdad

1. Crea en la interfaz un proyecto llamado «Prueba de persistencia» y un experimento.
2. Ejecuta:

```bash
docker compose down
docker compose up -d --wait
```

3. Inicia sesión y comprueba el mismo registro y sus valores.

`down` retira contenedores y red, pero conserva el volumen con los datos. **`down -v` elimina los volúmenes y los datos**: no lo uses para resolver errores ni como parte del reinicio habitual.

Cambiar `POSTGRES_PASSWORD` en `.env` no cambia la contraseña de una BD que ya está inicializada. Mantén la configuración original o realiza una rotación explícita administrada; no borres datos para corregir credenciales.

## 6. Crear usuarios propios

```bash
docker compose exec app python -m app.cli create-user
```

La herramienta pide correo y una contraseña de 12 a 128 caracteres, con confirmación. No hay registro público ni contraseña de administrador predefinida. La demo es solo para el entorno local.

## 7. Repositorio y CI

Extrae el proyecto en una carpeta independiente antes de crear tu repositorio. Revisa `git status` y comprueba que `.env`, `.venv`, `data` y `dist` no se incluyen. La plantilla de `.github/workflows/ci.yml` ejecuta lint, pruebas con ambos motores y construcción de imagen en GitHub Actions cuando se encuentra en la raíz del repositorio.

El participante realiza sus commits y push siguiendo las indicaciones del docente. El agente no debe publicarlos por su cuenta. Consulta `docs/08-despliegue.md` para pasar de ejecución local a un servidor con HTTPS.

## Entrega avanzada

Todo lo de la ruta básica, más: Compose reproducible desde un clon limpio, migraciones ejecutadas, persistencia demostrada, pruebas sobre PostgreSQL, CI configurado en el repositorio independiente y un procedimiento de despliegue documentado. GitHub almacena el código; la app se ejecuta en un equipo o servidor con Docker.
