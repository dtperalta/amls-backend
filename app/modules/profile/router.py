import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.profile.models import PerfilAprendiz
from app.modules.profile.schemas import (
    PerfilAprendizCreate,
    PerfilAprendizOut,
    PerfilAprendizUpdate,
)

router = APIRouter()


@router.post("/", response_model=PerfilAprendizOut, status_code=201)
def crear_perfil(datos: PerfilAprendizCreate, db: Session = Depends(get_db)):
    existente = db.query(PerfilAprendiz).filter_by(user_id=datos.user_id).first()
    if existente:
        raise HTTPException(400, "Ya existe un perfil para este usuario")

    perfil = PerfilAprendiz(**datos.model_dump())
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


@router.get("/{user_id}", response_model=PerfilAprendizOut)
def obtener_perfil(user_id: uuid.UUID, db: Session = Depends(get_db)):
    perfil = db.query(PerfilAprendiz).filter_by(user_id=user_id).first()
    if not perfil:
        raise HTTPException(404, "Perfil no encontrado")
    return perfil


@router.put("/{user_id}", response_model=PerfilAprendizOut)
def actualizar_perfil(
    user_id: uuid.UUID, datos: PerfilAprendizUpdate, db: Session = Depends(get_db)
):
    perfil = db.query(PerfilAprendiz).filter_by(user_id=user_id).first()
    if not perfil:
        raise HTTPException(404, "Perfil no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(perfil, campo, valor)

    db.commit()
    db.refresh(perfil)
    return perfil
