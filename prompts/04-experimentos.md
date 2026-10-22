# 04 · Experimentos, filtros y permisos

Punto de partida: proyectos funcionales o `01-proyectos`.

```text
Implementa app/routes/experiments.py siguiendo el contrato existente.

GET/POST /api/projects/{project_id}/experiments.
GET/PUT/DELETE /api/experiments/{experiment_id}.
GET permite el parámetro opcional model, con coincidencia exacta.

Usa ExperimentInput y ExperimentOut. Comprueba la propiedad del proyecto
antes de listar o crear. Para consultar, editar y borrar un experimento,
recorre su relación con Project y verifica al usuario autenticado.
Los IDs ajenos o inexistentes devuelven 404. No aceptes project_id o
user_id extras dentro del JSON ni cambies un experimento de propietario.

Conecta las acciones de la interfaz y conserva mensajes, confirmación de
borrado y estados vacíos. Comprueba que /api/summary cuenta datos propios
y que eliminar un proyecto con experimentos sigue devolviendo 409.

Ejecuta tests/test_domain.py y tests/test_auth.py. Corrige fallos con cambios
mínimos. Demuestra crear, editar, filtrar y eliminar; prueba además valores
inválidos y acceso por ID ajeno. No alteres la autenticación de la plantilla.
```
