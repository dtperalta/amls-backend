"""
Módulo: ML Recommender Service
================================
Mapea a "ML Recommender Service" / "Python Recommender" en la Vista
de Componentes y Vista de Despliegue de la propuesta.

Responsabilidad (RF-1, CON-6, UC-3):
- Adaptación estratégica a largo plazo: genera rutas de aprendizaje
  personalizadas a partir del perfil del estudiante.

Este es el módulo con más probabilidad de separarse primero en un
microservicio propio (Docker: ML Service) en la tesis, porque su
carga de cómputo (inferencia) es distinta a la de los otros dos.
Por eso su interfaz pública (service.py, cuando se agregue) debe
mantenerse limpia desde ahora: recibe datos, devuelve una
recomendación, sin depender de detalles internos de "content" o
"profile".
"""
