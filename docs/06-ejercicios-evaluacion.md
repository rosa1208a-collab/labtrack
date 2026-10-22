# Ejercicios, entrega y rúbrica

## Ejercicio 1 · Una petición completa

Crea «Clasificación de materiales». En Network localiza `POST /api/projects`, identifica los campos enviados y el ID recibido. Abre el endpoint del código, el validador y el modelo. Explica qué parte se ejecuta en el navegador y cuál en el servidor.

Entrega: captura de la pantalla y explicación de cinco líneas. No incluyas cookies, contraseñas ni tokens en capturas de cabeceras.

## Ejercicio 2 · Reglas y aislamiento

1. Registra un experimento con modelo `RandomForest`, dataset `materiales-v1`, métrica `F1` y valor `0.84`.
2. Cambia el valor a `0.87` y consulta nuevamente el registro.
3. Filtra por `RandomForest`, después por un modelo inexistente y finalmente limpia el filtro.
4. Intenta borrar el proyecto: debe rechazarlo mientras contenga experimentos.
5. En otra sesión, usa a Luis. El proyecto de Ana no aparece.
6. Ejecuta la prueba que intenta acceder al proyecto ajeno por ID. Espera 404.

Entrega: resultado de la prueba y explicación de autenticación frente a autorización.

## Ejercicio 3 · Persistencia y reproducción

Básica: reinicia Uvicorn y recupera el experimento. Avanzada: ejecuta `docker compose down` y `docker compose up -d --wait`; recupera el mismo experimento. Explica por qué `down -v` tendría otro resultado.

Pide a otra persona ejecutar una copia limpia siguiendo tu README. No compartas tu `.env`; debe generar el suyo. Una configuración nueva crea una BD diferente, por lo que se esperan datos iniciales, no los registros de tu equipo.

## Ejercicio 4 · Cambio de requisito

Añade a los experimentos un campo `status` con valores `planned`, `completed` y `discarded`, predeterminado `completed` para los registros existentes.

Debe incluir: modelo, nueva migración, validación, formulario, respuesta de API, columna visible y una prueba que rechace estados desconocidos. Aplica la migración conservando un experimento creado antes del cambio.

No se acepta eliminar la BD y volverla a crear. Explica por qué una migración es distinta de modificar únicamente una clase Python.

## Ejercicio 5 · Diagnóstico

El docente entrega un fallo de forma controlada en una copia: nombre de campo diferente entre frontend y API, URL de BD incorrecta o migración pendiente. Identifica el síntoma, reproduce, observa la respuesta/log, corrige lo mínimo y vuelve a comprobar. No expongas credenciales al copiar los logs al agente.

## Rúbrica de 100 puntos

| Criterio | Puntos | Evidencia |
|---|---:|---|
| Requisitos y explicación de arquitectura | 15 | Explica petición, capas y ERD |
| CRUD y relaciones | 25 | Flujo completo y regla de eliminación |
| Autenticación, permisos y validación | 20 | Dos usuarios, rechazo de datos inválidos y acceso ajeno |
| Pruebas y diagnóstico | 15 | Suite pasando y explicación de una corrección |
| Persistencia y reproducción | 15 | Reinicio sin perder datos y arranque desde copia limpia |
| README y demostración | 10 | Otra persona puede seguir las instrucciones |

En avanzada, reproducción exige Compose y pruebas con PostgreSQL. En básica, exige entorno virtual y SQLite. La versión entregada debe identificarse: usar la solución de referencia no demuestra por sí mismo autoría de un cambio.

## Lista de entrega

- [ ] README con versión de Python, preparación, arranque y pruebas.
- [ ] Diagrama de arquitectura y ERD actualizados.
- [ ] CRUD de proyectos y experimentos.
- [ ] Dos usuarios y permisos comprobados.
- [ ] Datos conservados tras reiniciar.
- [ ] Pruebas sin modificaciones que debiliten su objetivo.
- [ ] `.env`, tokens, contraseñas, BD y `.venv` fuera del repositorio.
- [ ] Avanzada: Dockerfile, Compose, migraciones y CI en la raíz del repositorio independiente.
- [ ] Una mejora propia explicada.
