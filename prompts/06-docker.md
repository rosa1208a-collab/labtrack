# 06 · Docker, PostgreSQL y reproducción

Punto de partida: solución funcional. La infraestructura ya está preparada para poder usar Docker desde el inicio; este ejercicio exige entenderla y comprobarla.

```text
Lee Dockerfile, compose.yaml y docs/04-ruta-avanzada.md.
Explica cada servicio, la red, los puertos y el volumen. Distingue app,
db y migrate de los servicios del perfil test.

Comprueba: usuario sin privilegios, dependencias e imágenes fijadas,
espera de PostgreSQL saludable, migración terminada antes de app,
ausencia de reload de desarrollo y BD sin puerto público.

Ejecuta docker compose config --quiet, construye y arranca el proyecto,
revisa healthchecks y ejecuta las pruebas del perfil test.
Usa exclusivamente la BD de prueba aislada para la suite.

Demuestra persistencia: crea un registro, ejecuta down sin -v, vuelve a
levantar y recupera el mismo registro. No elimines volúmenes.

Si Docker no está disponible, describe la comprobación pendiente y continúa
con tareas independientes; no inventes que el despliegue pasó.
Explica qué falta para publicar con HTTPS en un servidor. No publiques
ni contrates infraestructura, ni hagas commits o push.
```
