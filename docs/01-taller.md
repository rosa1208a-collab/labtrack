# Guía del taller

**Del prompt al despliegue: desarrollo de software con agentes de IA.** MiMETi, 21 de octubre de 2026, 15:00–19:00, sede UPQ. Facilitador: Mtro. José Javier Moya Moya.

## Resultado esperado

Construir y explicar el recorrido: persona → interfaz → petición HTTP → backend → validación y permisos → base de datos → respuesta → pantalla. Al finalizar, otra persona debe poder ejecutar el proyecto con sus instrucciones.

La IA ayuda a analizar requisitos, diseñar, escribir código, probar y depurar. La aplicación no necesita contratar una API de IA. Cada participante debe revisar lo que el agente cambia y comprobar su comportamiento.

## El caso: LabTrack

Una persona que trabaja con datos tiene experimentos repartidos entre notebooks y notas. Necesita registrar proyectos, versiones de datasets, modelos, métricas y observaciones en una bitácora consultable.

Ejemplo: proyecto «Clasificación de materiales», experimento «Línea base», modelo «RandomForest», dataset «materiales-v1», métrica «F1», valor `0.84`. Registrar el valor no ejecuta el modelo. Evita comparar valores de métricas diferentes como si fueran equivalentes.

## Dos rutas, una aplicación

| Aspecto | Básica | Avanzada |
|---|---|---|
| Conocimientos iniciales | Archivos, terminal y nociones de Python | Lo anterior, Git y Docker |
| Interfaz/API | HTML, CSS, JS y FastAPI | Las mismas |
| Datos | SQLite en archivo local | PostgreSQL en un servicio de Compose |
| Arranque | Entorno virtual y Uvicorn | Construcción de imagen y Compose |
| Entrega | CRUD funcional, pruebas y README | Lo anterior, persistencia, migraciones, CI y despliegue reproducible |

En ambas rutas se enseñan frontend, backend, API, persistencia, autenticación y autorización. Saber Docker no sustituye estos conceptos.

## Casos de uso

1. Como usuario, inicio sesión para acceder a mis proyectos.
2. Como usuario, creo un proyecto para agrupar experimentos.
3. Como usuario, registro un experimento y su resultado para consultarlo después.
4. Como usuario, modifico observaciones sin alterar experimentos ajenos.
5. Como usuario, filtro por modelo para localizar resultados concretos.
6. Como usuario, consulto cuántos proyectos y experimentos tengo.
7. Como usuario, elimino un experimento incorrecto y después un proyecto vacío.

## Otras ideas que reutilizan el aprendizaje

| Idea | Entidades | Regla interesante |
|---|---|---|
| Préstamos de laboratorio | Usuario, equipo, préstamo | Un equipo no puede tener dos préstamos activos |
| Mesa de ayuda | Usuario, solicitud, comentario | Solo el responsable puede cambiar ciertos estados |
| Inventario | Producto, movimiento | Una salida no puede dejar existencias negativas |
| Reciclaje | Material, entrega | Conservar unidades y fecha al agregar cantidades |
| Catálogo de datasets | Dataset, versión, responsable | Una versión conserva su origen y descripción |

Estas variantes se proponen después del primer flujo funcional. Durante el taller se usa un caso común para compartir soluciones y puntos de recuperación.

## Método de trabajo

1. Define qué se debe observar cuando una función esté terminada.
2. Pide un cambio pequeño al agente.
3. Revisa los archivos que cambió.
4. Ejecuta la aplicación y las comprobaciones.
5. Explica con tus palabras qué hace el código.
6. Conserva una versión que funcione antes de continuar.

Fórmula para pedir trabajo: **contexto + cambio concreto + restricciones + criterio de aceptación + comprobación**.

## Fuera del alcance de cuatro horas

Entrenamiento de modelos, subida de archivos, recuperación de contraseña por correo, registro público, pagos, equipos compartidos, microservicios y aplicaciones móviles. React puede ser una ampliación posterior sobre la misma API.
