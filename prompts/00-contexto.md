# 00 · Contexto común

Pega este bloque al comenzar o al cambiar de conversación con el agente.

```text
Estoy aprendiendo desarrollo web a partir de Python. Trabajaremos sobre LabTrack,
una bitácora de proyectos y experimentos de análisis de datos.

Lee AGENTS.md, README.md, ETAPA.md si existe y docs/02-arquitectura.md.
Inspecciona los archivos antes de proponer cambios. Conserva mi trabajo.

Stack acordado: HTML/CSS/JavaScript, FastAPI, SQLAlchemy, Alembic;
SQLite para la ruta básica y PostgreSQL con Docker Compose para la avanzada.
La interfaz y la API comparten origen.

La plantilla trae autenticación real, modelos, validadores, migraciones,
interfaz y pruebas. Los endpoints con 501 son ejercicios pendientes.
No reemplaces sesiones o persistencia por datos fijos, memoria o localStorage.

Implementa únicamente la etapa que te indique. Mantén el contrato de API.
Aplica permisos en el backend y obtiene el propietario desde la sesión.
Conserva CSRF, cookies HttpOnly, Argon2 y la expiración/revocación de sesiones.

No publiques secretos ni muestres .env completo. No borres bases ni volúmenes.
No hagas commits, push, ramas, PR ni despliegues por tu cuenta.
No borres pruebas ni cambies sus expectativas para ocultar fallos.

Al terminar: explica qué cambió, cómo probarlo, qué comprobaste realmente
y qué no pudiste comprobar. Usa lenguaje sencillo y relaciona los archivos
con el recorrido de una petición.
```
