# Guía docente · Cuatro horas

## Preparación

1. Ejecuta la solución desde una carpeta limpia usando los mismos comandos del grupo.
2. Genera los tres paquetes con `python scripts/package_workshop.py`.
3. Distribuye `00-inicio`; conserva `01-proyectos` y `02-completo` como recuperación y referencia.
4. Comprueba un equipo Windows y otro macOS/Linux antes del taller. La validación incluida describe los entornos efectivamente probados; no presupongas que todos los sistemas del grupo están preparados.
5. Para Docker, pide descargar imágenes y construir la plantilla antes de llegar.
6. Ten los ZIP y dependencias necesarias accesibles si falla Internet. Un ZIP por sí solo no contiene paquetes Python ni imágenes Docker.
7. Si habrá URL pública, prepara previamente servidor, dominio, HTTPS y cuentas. Las cuatro horas no incluyen contratar infraestructura.
8. Comprueba acceso a la herramienta de IA. No prometas cuotas ilimitadas de planes gratuitos.

La plantilla inicial ya trae autenticación, modelos, migración y frontend. Proyectos y experimentos responden 501. Es un esqueleto intencional: el grupo conecta las pantallas con operaciones reales. La solución completa sirve para estudiar y recuperar, no como evidencia de que el alumno implementó todo.

## Agenda

| Hora | Actividad | Evidencia |
|---|---|---|
| 15:00–15:15 | Verificar entorno y abrir plantilla | Acceso de usuario funcionando |
| 15:15–15:30 | Introducción preparada sobre LLM y agentes | Entender qué delegar y qué verificar |
| 15:30–15:50 | Requisitos, arquitectura y ERD | Explicar qué sucede al guardar |
| 15:50–16:30 | Primer flujo: proyectos | Registro persistente creado desde la interfaz |
| 16:30–16:40 | Pausa | |
| 16:40–17:25 | Experimentos, filtros y permisos | CRUD completo |
| 17:25–17:50 | Pruebas y depuración | Corregir un fallo con evidencia |
| 17:50–18:35 | Reproducción por rutas | Reinicio con SQLite o recreación con Compose |
| 18:35–19:00 | Demostraciones y cierre | Aplicación y explicación de cinco minutos |

## Guion de demostración

1. Muestra LabTrack completo durante dos minutos: entrar, crear, guardar y consultar.
2. Dibuja navegador → API → BD. Pregunta dónde se valida la información.
3. Abre Network/Red y crea un proyecto. Identifica URL, método POST, JSON enviado y respuesta 201.
4. Relaciona la petición con `app/routes/projects.py`, el esquema y la tabla.
5. Cierra y vuelve a abrir la aplicación: el registro continúa.
6. Cambia de usuario: sus datos son diferentes.
7. Ejecuta una prueba que intente pedir el ID de otro usuario. Explica por qué el backend responde 404.
8. En Docker muestra `docker compose ps`, los logs de migración y el volumen.

## Preguntas de comprensión

- ¿Por qué validar solo en el formulario no es suficiente?
- ¿Dónde decide el sistema a qué usuario pertenece un proyecto?
- ¿Qué diferencia hay entre una imagen, un contenedor y un volumen?
- ¿Qué ocurre si la BD todavía no está lista cuando arranca la app?
- ¿Qué cambia al pasar de SQLite a PostgreSQL y qué se conserva?
- ¿Por qué añadir un campo al formulario no modifica por sí solo la tabla?
- ¿Por qué un repositorio en GitHub no significa que la API esté publicada?

## Trabajo en parejas

Una persona dirige el agente y la otra revisa requisitos y comprueba resultados. Intercambian los papeles al terminar proyectos. Quien avanza rápido hace el cambio de requisito del ejercicio 4, sin añadir complejidad al punto de partida del resto.

## Recuperación sin perder el grupo

Si una persona lleva más de diez minutos bloqueada, debe explicar qué intentó, conservar su carpeta y continuar desde el ZIP siguiente en otra carpeta. No se pide al agente reescribir todo ni borrar el volumen. Los checkpoints permiten continuar aunque se agote una cuota de IA.

En `00-inicio` y `01-proyectos`, la respuesta 501 y los fallos de dominio pendientes son esperados. Las pruebas de autenticación deben pasar. Al completar la etapa final debe pasar toda la suite.

## Cierre

Cada equipo demuestra un cambio propio y explica una petición completa. El docente revisa comprensión, pruebas y reproducibilidad además de la apariencia. Publicar el código lo realiza el alumno después de revisar que no incluya secretos.
