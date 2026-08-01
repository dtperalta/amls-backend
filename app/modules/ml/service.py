"""
Lógica de recomendación del ML Recommender Service (v2).

A diferencia de la v1 (basada solo en perfil autodeclarado), este
modelo usa el desempeño REAL del estudiante en el quiz diagnóstico
como señal dominante, resolviendo la inconsistencia detectada entre
la recomendación y el resultado real del quiz.
"""
from pathlib import Path

import joblib
import pandas as pd

_RUTA_MODELO = Path(__file__).parent / "modelo_recomendador.joblib"
_datos_modelo = joblib.load(_RUTA_MODELO)

_modelo = _datos_modelo["modelo"]
_encoders = _datos_modelo["encoders"]


def recomendar_nivel_dificultad(
    nivel_lectura: str,
    porcentaje_acierto_quiz: float,
    cantidad_lecciones_dominadas: int,
) -> str:
    fila = pd.DataFrame(
        {
            "nivel_lectura": [_encoders["nivel_lectura"].transform([nivel_lectura])[0]],
            "porcentaje_acierto_quiz": [porcentaje_acierto_quiz],
            "cantidad_lecciones_dominadas": [cantidad_lecciones_dominadas],
        }
    )
    prediccion = _modelo.predict(fila)[0]
    return _encoders["nivel_dificultad_recomendado"].inverse_transform([prediccion])[0]
