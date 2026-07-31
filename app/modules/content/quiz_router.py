import random
import uuid
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_verified_user_id
from app.modules.content.quiz_models import PreguntaQuiz, ResultadoQuizDiagnostico
from app.modules.content.quiz_schemas import (
    EnviarQuizRequest,
    PreguntaQuizCreate,
    PreguntaQuizOut,
    ResultadoQuizOut,
)

router = APIRouter()


@router.post("/preguntas", response_model=PreguntaQuizOut, status_code=201)
def crear_pregunta(datos: PreguntaQuizCreate, db: Session = Depends(get_db)):
    pregunta = PreguntaQuiz(**datos.model_dump())
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    return pregunta


@router.get("/", response_model=list[PreguntaQuizOut])
def obtener_quiz(db: Session = Depends(get_db)):
    preguntas = db.query(PreguntaQuiz).all()
    random.shuffle(preguntas)  # mezcladas en cada solicitud, no en orden fijo
    return preguntas


@router.post("/enviar", response_model=ResultadoQuizOut)
def enviar_quiz(
    datos: EnviarQuizRequest,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_verified_user_id),
):
    existente = db.query(ResultadoQuizDiagnostico).filter_by(user_id=current_user_id).first()
    if existente:
        raise HTTPException(400, "Ya completaste el quiz diagnóstico anteriormente")

    ids_preguntas = [r.pregunta_id for r in datos.respuestas]
    preguntas_db = db.query(PreguntaQuiz).filter(PreguntaQuiz.id.in_(ids_preguntas)).all()
    mapa_preguntas = {p.id: p for p in preguntas_db}

    # 2 correctas de 2 en una lección = "dominada"
    correctas_por_recurso = defaultdict(int)
    total_correctas = 0

    for respuesta in datos.respuestas:
        pregunta = mapa_preguntas.get(respuesta.pregunta_id)
        if not pregunta:
            continue
        if respuesta.indice_seleccionado == pregunta.indice_correcta:
            correctas_por_recurso[pregunta.recurso_id] += 1
            total_correctas += 1

    recursos_dominados = [
        recurso_id for recurso_id, aciertos in correctas_por_recurso.items() if aciertos >= 2
    ]

    resultado = ResultadoQuizDiagnostico(
        user_id=current_user_id,
        recursos_dominados=recursos_dominados,
    )
    db.add(resultado)
    db.commit()
    db.refresh(resultado)

    return ResultadoQuizOut(
        recursos_dominados=recursos_dominados,
        total_correctas=total_correctas,
        total_preguntas=len(datos.respuestas),
    )


@router.get("/resultado", response_model=ResultadoQuizOut | None)
def obtener_resultado_propio(
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_verified_user_id),
):
    resultado = db.query(ResultadoQuizDiagnostico).filter_by(user_id=current_user_id).first()
    if not resultado:
        return None
    return ResultadoQuizOut(
        recursos_dominados=resultado.recursos_dominados,
        total_correctas=sum(1 for _ in resultado.recursos_dominados),  # aproximado
        total_preguntas=12,
    )
