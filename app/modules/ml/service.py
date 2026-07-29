"""
Lógica de recomendación del ML Recommender Service.

ESTADO ACTUAL: placeholder con reglas simples (if/else), NO es el
modelo de Machine Learning real todavía. Eso corresponde al Sprint 5
(dataset sintético + entrenamiento con Scikit-learn + export a
formato usable), según el plan de trabajo de la propuesta.

Esta función mantiene el mismo contrato (mismos parámetros de entrada,
mismo tipo de salida) que tendrá la versión real. Cuando se entrene el
modelo en el Sprint 5, solo se reemplaza el cuerpo de esta función —
el router y todo lo que lo consume (incluida la app Android) no
necesitan cambiar.
"""


def recomendar_nivel_dificultad(
    grado_perdida_auditiva: str,
    preferencia_comunicativa: str,
    nivel_lectura: str,
) -> str:
    """Regla temporal: recomienda dificultad según nivel de lectura."""
    reglas = {
        "Básico": "Leve",
        "Intermedio": "Moderada",
        "Avanzado": "Avanzada",
    }
    return reglas.get(nivel_lectura, "Leve")
