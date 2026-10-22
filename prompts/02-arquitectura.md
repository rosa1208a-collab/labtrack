# 02 · Arquitectura, ERD y contrato

```text
Inspecciona la plantilla y docs/02-arquitectura.md. Explícame cómo se reparten
las responsabilidades entre frontend, API, validación, autenticación y BD.

Entrega un diagrama Mermaid de arquitectura y un ERD que correspondan
al código. Distingue las entidades de negocio de las tablas de soporte.

Para crear un experimento, identifica: ruta HTTP, método, JSON de entrada,
respuesta, esquema de validación, comprobación de propietario y tabla final.
Explica por qué el usuario_id no debe decidirlo el navegador.

Explica claves primarias, claves foráneas, migraciones y la regla de borrado
de proyectos con experimentos usando ejemplos de LabTrack.

Conserva las tecnologías y rutas acordadas. No propongas microservicios ni
añadas capas sin una responsabilidad concreta. Todavía no cambies código.
```

Comprueba: puedes señalar la ruta del dato y explicar qué ocurre si un ID pertenece a otra persona.
