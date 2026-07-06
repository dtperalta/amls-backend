import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


class PerfilAprendiz(Base):
    __tablename__ = "perfil_aprendiz"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)

    grado_perdida_auditiva = Column(String, nullable=False, default="Leve")
    preferencia_comunicativa = Column(String, nullable=False, default="Subtítulos")
    nivel_lectura = Column(String, nullable=False, default="Básico")
    requiere_alto_contraste = Column(Boolean, nullable=False, default=False)
    tamano_subtitulos = Column(Integer, nullable=False, default=18)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
