import datetime
import uuid
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PerfilAprendizBase(BaseModel):
    grado_perdida_auditiva: str = "Leve"
    preferencia_comunicativa: str = "Subtítulos"
    nivel_lectura: str = "Básico"
    requiere_alto_contraste: bool = False
    tamano_subtitulos: int = 18


class PerfilAprendizCreate(PerfilAprendizBase):
    pass


class PerfilAprendizUpdate(PerfilAprendizBase):
    pass


class PerfilAprendizOut(PerfilAprendizBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID


class HistorialInteraccionCreate(BaseModel):
    recurso_id: Optional[str] = None
    tipo_evento: str
    metadata_extra: Optional[dict[str, Any]] = None


class HistorialInteraccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    recurso_id: Optional[str]
    tipo_evento: str
    metadata_extra: Optional[dict[str, Any]]
    created_at: datetime.datetime
