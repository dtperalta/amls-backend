"""
Modelos del quiz diagnóstico inicial (12 preguntas, 2 por lección).

Resultado por lección: "dominada" o "no dominada" — una capa simple y
directa, separada del ML Recommender (Árbol de Decisión). Ver
ARCHITECTURE.md para la justificación de esta separación.
"""
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


class PreguntaQuiz(Base):
    __tablename__ = "preguntas_quiz"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recurso_id = Column(
        String,
        ForeignKey("recursos_educativos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    enunciado = Column(String, nullable=False)
    opciones = Column(JSONB, nullable=False)  # ["opción A", "opción B", "opción C", "opción D"]
    indice_correcta = Column(Integer, nullable=False)  # 0-3


class ResultadoQuizDiagnostico(Base):
    __tablename__ = "resultados_quiz_diagnostico"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # se toma una sola vez
        index=True,
    )
    recursos_dominados = Column(JSONB, nullable=False)  # ["LECCION-2", "LECCION-4"]
    completado_en = Column(DateTime(timezone=True), server_default=func.now())
