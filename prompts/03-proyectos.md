# 03 · Primer flujo completo: proyectos

Punto de partida: `00-inicio`.

```text
Implementa el CRUD de proyectos en la plantilla LabTrack, sustituyendo
los endpoints 501 de app/routes/projects.py.

Respeta estas rutas:
GET/POST /api/projects y GET/PUT/DELETE /api/projects/{project_id}.
Usa ProjectInput y ProjectOut. El propietario sale de get_current_user.
Solo lista y modifica proyectos propios; un ID inexistente o ajeno da 404.
El borrado de un proyecto con experimentos devuelve 409.

Primero termina crear y listar: conecta el formulario, guarda en la BD
y vuelve a consultar. Después completa editar y eliminar.
Conserva la interfaz, autenticación, CSRF y esquema existentes.

Crea una función owned_project(db, project_id, user_id) reutilizable
por la siguiente etapa. No aceptes user_id en el cuerpo de la petición.
La etapa de experimentos puede seguir respondiendo 501.

Ejecuta las pruebas de autenticación y comprueba manualmente crear,
consultar, editar y eliminar un proyecto vacío. Comprueba que el registro
se conserva después de reiniciar. Indica qué pruebas de dominio dependen
todavía de implementar experimentos, sin borrarlas ni debilitarlas.

Explica el recorrido desde Guardar hasta el commit de la transacción.
```

Comprueba: no se aceptan listas fijas ni guardado en localStorage. Si la sección de experimentos responde 501, es la siguiente etapa.
