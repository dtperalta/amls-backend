import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class RecursoEducativo(Base):
    __tablename__ = "recursos_educativos"

    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    tipo_formato = Column(String, nullable=False)
    url_descarga = Column(String, nullable=True)
    tiene_lengua_senas = Column(Boolean, nullable=False, default=False)
    nivel_dificultad = Column(String, nullable=False)
    transcripcion = Column(Text, nullable=True)


class ArchivoRecurso(Base):
    __tablename__ = "archivos_recurso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recurso_id = Column(
        String,
        ForeignKey("recursos_educativos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tipo_archivo = Column(String, nullable=False)  # "video" | "subtitulos" | "infografia"
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

