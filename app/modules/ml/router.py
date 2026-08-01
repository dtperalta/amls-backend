from fastapi import APIRouter

from app.modules.ml.schemas import RecomendacionInput, RecomendacionOutput
from app.modules.ml.service import recomendar_nivel_dificultad

router = APIRouter()


@router.post("/recomendar", response_model=RecomendacionOutput)
def recomendar(datos: RecomendacionInput):
    nivel = recomendar_nivel_dificultad(
        datos.nivel_lectura,
        datos.porcentaje_acierto_quiz,
        datos.cantidad_lecciones_dominadas,
    )
    return RecomendacionOutput(nivel_dificultad_recomendado=nivel)
