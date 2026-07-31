import uuid

from pydantic import BaseModel, ConfigDict


class PreguntaQuizOut(BaseModel):
    """Nunca incluye indice_correcta — el cliente no debe conocerlo de antemano."""
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    recurso_id: str
    enunciado: str
    opciones: list[str]


class RespuestaQuizItem(BaseModel):
    pregunta_id: uuid.UUID
    indice_seleccionado: int


class EnviarQuizRequest(BaseModel):
    respuestas: list[RespuestaQuizItem]


class ResultadoQuizOut(BaseModel):
    recursos_dominados: list[str]
    total_correctas: int
    total_preguntas: int


class PreguntaQuizCreate(BaseModel):
    recurso_id: str
    enunciado: str
    opciones: list[str]
    indice_correcta: int
