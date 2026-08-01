from pydantic import BaseModel


class RecomendacionInput(BaseModel):
    nivel_lectura: str
    porcentaje_acierto_quiz: float
    cantidad_lecciones_dominadas: int


class RecomendacionOutput(BaseModel):
    nivel_dificultad_recomendado: str
