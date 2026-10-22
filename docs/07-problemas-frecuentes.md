# Resolución de problemas

## «No module named…» o instala paquetes en otro proyecto

Sitúate donde están `requirements-dev.txt` y `alembic.ini`. Activa el entorno y ejecuta `python -m pip install -r requirements-dev.txt`. Usa siempre `python -m pip` para que pip corresponda al intérprete seleccionado. En Windows puedes usar `.\.venv\Scripts\python.exe` sin activar.

## Python antiguo

Comprueba `python --version`. El taller requiere 3.11+ y recomienda 3.12. En macOS puede coexistir un `python3` antiguo con `python3.12`; usa el segundo para crear el entorno.

## PowerShell bloquea Activate.ps1

Ejecuta directamente `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` y los demás comandos con ese mismo Python. No es necesario cambiar la política de todo el sistema.

## Puerto ocupado

No ejecutes ambas rutas simultáneamente en 8010. Detén la anterior con Ctrl+C o `docker compose stop app`. Si eliges otro puerto, cambia también `ALLOWED_ORIGINS`; para Docker cambia `APP_PORT`. No cierres procesos de otros proyectos al azar.

## 401 al abrir la API

La sesión no existe o caducó. Inicia sesión desde la interfaz. En una petición de prueba conserva la cookie; no basta con enviar un correo. Después de cinco contraseñas fallidas la cuenta espera quince minutos antes de aceptar otro intento.

## 403 por origen o CSRF

Usa exactamente `http://127.0.0.1:8010` o `http://localhost:8010`, según la configuración. Un puerto diferente es un origen diferente. Los POST/PUT/DELETE autenticados necesitan la cookie y `X-CSRF-Token`; el frontend los envía automáticamente. No elimines la protección para hacer funcionar una petición manual.

## 404 al usar un ID

El recurso no existe o pertenece a otra persona. Es un comportamiento esperado; el servidor no revela datos ajenos.

## 409 al eliminar un proyecto

Todavía contiene experimentos. Elimina primero esos registros si esa es tu intención. No cambies automáticamente la regla a borrado en cascada.

## 422 al guardar

Inspecciona `detail` en la respuesta. El backend rechaza nombres vacíos, números no válidos y campos desconocidos. Comprueba el contrato y el JSON antes de cambiar código.

## 501 en la plantilla inicial

Es un ejercicio pendiente. Lee `ETAPA.md`: en `00-inicio` faltan proyectos y experimentos; en `01-proyectos` solo experimentos. Usa el prompt de la etapa. No reemplaces 501 por datos inventados o localStorage.

## «no such table» / «relation does not exist»

Aplica `python -m alembic upgrade head` en básica. En Docker consulta `docker compose logs migrate` y corrige la causa antes de volver a arrancar. No agregues `create_all()` como sustituto de las migraciones del taller.

## Docker no responde

Abre tu motor de Docker y comprueba `docker info` y `docker compose version`. Si el equipo no tiene el motor listo, continúa con SQLite y conserva la ruta avanzada para después.

## Cambié el código y Docker muestra lo mismo

Ejecuta `docker compose up -d --build --wait`. La imagen contiene el código; el Compose no monta tu carpeta como volumen ni usa recarga de desarrollo.

## PostgreSQL rechaza una contraseña después de editar .env

El volumen existente conserva las credenciales con las que PostgreSQL se inicializó. Cambiar una variable no rota la contraseña de la BD. Recupera la configuración correspondiente o pide una rotación administrada. `down -v` destruiría los datos.

## Pruebas con PostgreSQL

Usa el perfil de prueba documentado. `TEST_DATABASE_URL` debe apuntar a una base desechable terminada en `_test`; nunca a `labtrack`. Las fixtures recrean sus tablas.

## Cuota de IA o red agotada

Guarda tu carpeta, explica el último estado funcional y usa el siguiente ZIP de recuperación. Los paquetes Python y las imágenes deben descargarse antes; los ZIP de código no permiten instalar dependencias sin conexión por sí solos.

## GitHub Actions no se ejecuta

El workflow debe estar en `.github/workflows/ci.yml` en la raíz de un repositorio propio. GitHub no ejecuta workflows anidados en `talleres/labtrack/.github` dentro de `grades_ai`. En los checkpoints incompletos las pruebas de dominio fallan hasta completar la práctica.
