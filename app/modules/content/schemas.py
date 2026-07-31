import uuid

from pydantic import BaseModel, ConfigDict


class RecursoEducativoBase(BaseModel):
    titulo: str
    tipo_formato: str
    url_descarga: str | None = None
    tiene_lengua_senas: bool = False
    nivel_dificultad: str
    transcripcion: str | None = None


class RecursoEducativoCreate(RecursoEducativoBase):
    id: str


class RecursoEducativoOut(RecursoEducativoBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    url_subtitulos: str | None = None


class RecursoEducativoUpdate(BaseModel):
    titulo: str | None = None
    tipo_formato: str | None = None
    tiene_lengua_senas: bool | None = None
    nivel_dificultad: str | None = None
    transcripcion: str | None = None


class ArchivoRecursoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    recurso_id: str
    tipo_archivo: str
    url: str

