# De ejecución local a despliegue

## Tres cosas diferentes

1. GitHub conserva y distribuye el código.
2. Docker Compose ejecuta la aplicación y la BD en un equipo.
3. Un servidor accesible, con dominio y HTTPS, publica la aplicación para otras personas.

GitHub Pages sirve sitios estáticos y no ejecuta esta API Python ni PostgreSQL. Referencia: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages/).

## Destino previsto para la práctica

Un servidor Linux administrado por el docente con Docker Compose y un proxy HTTPS ya configurado. La app escucha en `127.0.0.1:8010` y el proxy del mismo host reenvía las peticiones a esa dirección. La BD continúa sin puerto público.

Para varios equipos, asigna un nombre de proyecto Compose, un puerto local y un subdominio por equipo. No compartas credenciales administrativas entre participantes.

No se proporciona ni contrata un servidor con la plantilla. El costo y disponibilidad dependen de la infraestructura del docente. Este procedimiento es una guía para ese destino; el ensayo local de Docker no verifica DNS, TLS ni disponibilidad de un servidor remoto.

## Preparación del servidor

1. Copia o clona el repositorio independiente en una carpeta de despliegue.
2. Genera `.env` en el servidor con `python3 scripts/init_env.py`.
3. Cambia `ALLOWED_ORIGINS` al origen HTTPS real, por ejemplo `["https://labtrack.ejemplo.edu"]`.
4. Configura `SESSION_COOKIE_SECURE=true` y vacía `DEMO_PASSWORD`.
5. Conserva una contraseña PostgreSQL propia. No transfieras las credenciales de la demo.
6. Configura DNS y HTTPS en el proxy administrado y su destino `127.0.0.1:8010`.
7. Arranca:

```bash
docker compose up -d --build --wait
docker compose exec app python -m app.cli create-user
docker compose ps
```

No ejecutes `seed-demo` en un servidor público. El comando se rechaza cuando las cookies seguras están activadas. El proxy debe conservar el origen externo de la petición; no sustituyas la cabecera Origin por un valor arbitrario.

Comprueba mediante HTTPS: iniciar/cerrar sesión, crear un registro, permisos entre dos cuentas y persistencia. Si todavía usas HTTP local con `SESSION_COOKIE_SECURE=true`, el navegador puede no enviar la cookie; corrige el entorno en vez de debilitar la configuración del servidor publicado.

## Actualizaciones y migraciones

Haz una copia de seguridad antes de modificar el esquema. Para un único servidor y una ventana de mantenimiento breve:

```bash
docker compose build app migrate
docker compose stop app
docker compose run --rm migrate
docker compose up -d --wait app
```

Si la migración falla, conserva la copia de seguridad, revisa sus logs y resuelve el fallo antes de iniciar la nueva versión. No intentes arreglarlo eliminando el volumen. Una reversión de código puede requerir también un plan de compatibilidad del esquema.

## Copia de seguridad local del despliegue

En una terminal Linux/macOS, desde la carpeta del proyecto:

```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > labtrack-backup.dump
```

Guarda el archivo fuera del repositorio y protege su acceso: contiene los datos de usuarios y autenticación. Antes de confiar en el procedimiento, ensaya una restauración en una BD aparte. No basta con comprobar que el archivo existe.

## Límites del MVP

El control de intentos de acceso de la app es básico, por cuenta; una publicación con usuarios reales necesita además límites de tráfico en el proxy, mantenimiento de dependencias, copias de seguridad verificadas y monitoreo. No hay registro público, recuperación de contraseña, MFA, auditoría de acciones ni paginación. Estos son temas de una siguiente iteración, no funciones que se deban dar por implementadas.

Referencia de operación: [Compose en producción](https://docs.docker.com/compose/how-tos/production/).
