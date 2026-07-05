"""
Módulo: API Gateway
=====================
Mapea a "API Gateway" en la Vista de Componentes de la propuesta.

Responsabilidad:
- Punto de entrada único: agrega los routers de content, profile y ml.
- Autenticación y control de acceso centralizado (QA-14).

En el prototipo actual, esto es solo el router raíz de FastAPI que
incluye a los demás. En una futura separación a microservicios reales,
este módulo se convierte en un servicio propio (ej. con Kong, Nginx,
o un FastAPI dedicado) que reenvía peticiones a los servicios
independientes.
"""
