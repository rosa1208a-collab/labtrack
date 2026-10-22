# LabTrack: reglas para el agente del taller

- Lee `ETAPA.md` si existe, `README.md` y el prompt de la etapa antes de editar.
- Conserva los cambios de la persona. No hagas commits, push, ramas, PR ni despliegues por tu cuenta.
- Mantén Python/FastAPI, SQLAlchemy/Alembic, HTML/CSS/JavaScript y el contrato documentado.
- La ruta básica usa SQLite; la avanzada usa PostgreSQL con Docker Compose.
- Conserva la autenticación de la plantilla. No simules sesiones ni sustituyas la base de datos por memoria o localStorage.
- El propietario se obtiene de la sesión. Valida permisos en todas las operaciones, filtros y resúmenes.
- No publiques `.env`, contraseñas, datos locales ni tokens. No elimines volúmenes para resolver un error de migración.
- Implementa una etapa por vez. Explica qué cambiaste y ejecuta sus comprobaciones.
- Si una comprobación no puede ejecutarse, indícalo. No inventes resultados.
- No borres pruebas ni debilites criterios para hacer pasar la suite.
