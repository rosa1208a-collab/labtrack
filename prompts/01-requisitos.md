# 01 · Del problema a los requisitos

Objetivo: definir el comportamiento antes de programar.

```text
Actúa como analista de software y tutor. Una persona que trabaja con datos
necesita reunir proyectos y resultados de experimentos que hoy están
dispersos en notebooks y notas.

LabTrack permite iniciar/cerrar sesión, gestionar proyectos propios y
registrar sus experimentos. Cada experimento contiene nombre, modelo,
versión del dataset, nombre y valor de una métrica, y observaciones.
Incluye filtro exacto por modelo y resumen de cantidades propias.

No se puede eliminar un proyecto que todavía tenga experimentos.
Un usuario nunca puede consultar o modificar datos de otro, aunque cambie IDs.
Quedan fuera ejecución de modelos, subida de archivos y colaboración.

Lee los requisitos existentes y entrega:
1. Cinco historias de usuario con criterios Dado/Cuando/Entonces.
2. Reglas de negocio y dos ejemplos de datos inválidos.
3. Diferencia entre requisito funcional y no funcional, con ejemplos del caso.
4. Tres incrementos que puedan demostrarse en el navegador.
5. Supuestos pendientes, sin agregar funciones al alcance.

Todavía no escribas código ni modifiques archivos.
```

Comprueba: debe aparecer el caso de acceso por ID ajeno y el caso de reiniciar sin perder datos.
