# 07 · Cambiar un requisito sin perder datos

```text
Añade status a Experiment con valores planned, completed y discarded.
Los experimentos existentes deben conservarse y recibir completed.

Primero identifica qué cambia en modelo, validación, migración, respuesta
de API, formulario y tabla. Después implementa la modificación con una nueva
migración Alembic. No edites la migración inicial para simular que siempre
existió el campo y no elimines la BD ni el volumen.

Añade una prueba que rechace estados desconocidos y otra que demuestre
la conservación de un experimento anterior a la migración.
Aplica y comprueba el cambio con SQLite y, si está disponible, PostgreSQL.
Actualiza el ERD y el contrato. Explica qué cambiaría si solo agregáramos
un input en el frontend.
```
