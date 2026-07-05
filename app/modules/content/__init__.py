"""
Módulo: Content Manager
========================
Mapea a "Content Manager" en la Vista de Componentes de la propuesta
(Diana Peralta, CINVESTAV).

Responsabilidad (RF-6, RF-10, UC-7, UC-8):
- CRUD de recursos educativos (RecursoEducativo).
- Clasificación por nivel de dificultad y accesibilidad.

Regla de frontera:
Ningún otro módulo debe importar los modelos/tablas de este módulo
directamente. Si "profile" o "ml" necesitan datos de contenido, deben
llamar a funciones expuestas aquí (en service.py, cuando se agregue),
nunca hacer queries directas a sus tablas.

Esto es lo que permite, en la tesis, extraer este módulo a un
microservicio Docker independiente (como en la Vista de Despliegue
original) sin reescribir la lógica interna — solo se envuelve esta
misma interfaz en endpoints HTTP propios.
"""
