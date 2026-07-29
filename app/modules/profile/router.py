import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.profile.models import HistorialInteraccion, PerfilAprendiz
from app.modules.profile.schemas import (
    HistorialInteraccionCreate,
    HistorialInteraccionOut,
    PerfilAprendizCreate,
    PerfilAprendizOut,
    PerfilAprendizUpdate,
)

router = APIRouter()


@router.post("/", response_model=PerfilAprendizOut, status_code=201)
def crear_perfil(
    datos: PerfilAprendizCreate,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    existente = db.query(PerfilAprendiz).filter_by(user_id=current_user_id).first()
    if existente:
        raise HTTPException(400, "Ya existe un perfil para este usuario")

    perfil = PerfilAprendiz(user_id=current_user_id, **datos.model_dump())
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


@router.get("/", response_model=PerfilAprendizOut)
def obtener_perfil(
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    perfil = db.query(PerfilAprendiz).filter_by(user_id=current_user_id).first()
    if not perfil:
        raise HTTPException(404, "Perfil no encontrado")
    return perfil


@router.put("/", response_model=PerfilAprendizOut)
def actualizar_perfil(
    datos: PerfilAprendizUpdate,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):

    perfil = db.query(PerfilAprendiz).filter_by(user_id=current_user_id).first()
    if not perfil:
        raise HTTPException(404, "Perfil no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(perfil, campo, valor)

    db.commit()
    db.refresh(perfil)
    return perfil


@router.post("/historial/", response_model=HistorialInteraccionOut, status_code=201)
def registrar_evento(
    datos: HistorialInteraccionCreate,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    evento = HistorialInteraccion(user_id=current_user_id, **datos.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


@router.get("/historial/", response_model=list[HistorialInteraccionOut])
def obtener_historial(
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return (
        db.query(HistorialInteraccion)
        .filter_by(user_id=current_user_id)
        .order_by(HistorialInteraccion.created_at.desc())
        .all()
    )
