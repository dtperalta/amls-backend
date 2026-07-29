from pydantic import BaseModel


class RecomendacionInput(BaseModel):
    grado_perdida_auditiva: str
    preferencia_comunicativa: str
    nivel_lectura: str


class RecomendacionOutput(BaseModel):
    nivel_dificultad_recomendado: str
    es_placeholder: bool = True
