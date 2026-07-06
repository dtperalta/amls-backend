import uuid

from pydantic import BaseModel, ConfigDict


class PerfilAprendizBase(BaseModel):
    grado_perdida_auditiva: str = "Leve"
    preferencia_comunicativa: str = "Subtítulos"
    nivel_lectura: str = "Básico"
    requiere_alto_contraste: bool = False
    tamano_subtitulos: int = 18


class PerfilAprendizCreate(PerfilAprendizBase):
    user_id: uuid.UUID


class PerfilAprendizUpdate(PerfilAprendizBase):
    pass


class PerfilAprendizOut(PerfilAprendizBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
