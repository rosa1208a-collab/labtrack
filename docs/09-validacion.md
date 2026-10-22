# Comprobaciones realizadas

Fecha de preparación: 20 de octubre de 2026, zona America/Mexico_City.

## Evidencia ejecutada

| Entorno | Comprobación | Resultado |
|---|---|---|
| macOS, Python 3.12, SQLite | Suite completa | 24 pruebas aprobadas |
| Docker Linux, Python 3.12, SQLite + PostgreSQL 17 | Suite completa con los dos motores | 48 pruebas aprobadas |
| Docker Linux, Python 3.11, SQLite | Dependencias desde el ZIP y suite completa | 24 pruebas aprobadas |
| Código Python | Ruff | Sin errores |
| Compose | Construcción, arranque, migración y healthchecks | Servicios saludables; migración termina con código 0 |
| Navegador | Login, crear proyecto, crear experimento y resumen | Flujo visible correcto |
| Persistencia PostgreSQL | `down` sin eliminar volumen, nuevo arranque y recarga del navegador | Se recuperaron el proyecto y experimento creados |
| ZIP 00 y 01 en carpetas independientes | Configuración, migración, seed y pruebas de autenticación | Aprobados |
| ZIP 02 en carpeta independiente | Configuración, migración, seed y suite completa | Aprobado |
| Paquetes | Inspección de contenidos | Sin `.env`, datos, contraseñas generadas ni entornos virtuales |

## Cobertura de las pruebas

Sesiones, cierre y revocación, expiración, validación de origen, CSRF, intentos fallidos, acceso sin sesión, CRUD, aislamiento entre dos usuarios en todas las operaciones, filtros, resumen, valores inválidos, regla de borrado, persistencia entre instancias y migraciones repetibles.

## Alcance de la validación

No se ejecutó Windows ni GitHub Actions remoto; el workflow está preparado para un repositorio independiente. Tampoco se configuró un servidor público, dominio o HTTPS. La suite muestra un aviso de deprecación de Starlette sobre su adaptador de pruebas httpx; no impide los resultados anteriores.

Estos resultados corresponden a la solución de referencia. Las etapas incompletas mantienen pruebas de dominio que deben fallar hasta completar el ejercicio. Una modificación posterior exige volver a ejecutar las comprobaciones relacionadas.
