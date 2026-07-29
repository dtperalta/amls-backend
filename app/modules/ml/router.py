from fastapi import APIRouter

from app.modules.ml.schemas import RecomendacionInput, RecomendacionOutput
from app.modules.ml.service import recomendar_nivel_dificultad

router = APIRouter()


@router.post("/recomendar", response_model=RecomendacionOutput)
def recomendar(datos: RecomendacionInput):
    nivel = recomendar_nivel_dificultad(
        datos.grado_perdida_auditiva,
        datos.preferencia_comunicativa,
        datos.nivel_lectura,
    )
    return RecomendacionOutput(nivel_dificultad_recomendado=nivel)
