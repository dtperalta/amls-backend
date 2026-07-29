from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.content.models import ArchivoRecurso, RecursoEducativo
from app.modules.content.schemas import (
    ArchivoRecursoOut,
    RecursoEducativoCreate,
    RecursoEducativoOut,
    RecursoEducativoUpdate,
)
from app.modules.content.storage import subir_archivo

router = APIRouter()

TIPOS_PERMITIDOS = {"video", "subtitulos", "infografia"}


@router.post("/", response_model=RecursoEducativoOut, status_code=201)
def crear_recurso(datos: RecursoEducativoCreate, db: Session = Depends(get_db)):
    existente = db.query(RecursoEducativo).filter_by(id=datos.id).first()
    if existente:
        raise HTTPException(400, "Ya existe un recurso con ese id")

    recurso = RecursoEducativo(**datos.model_dump())
    db.add(recurso)
    db.commit()
    db.refresh(recurso)
    return recurso


@router.get("/", response_model=list[RecursoEducativoOut])
def listar_recursos(db: Session = Depends(get_db)):
    return db.query(RecursoEducativo).order_by(RecursoEducativo.id).all()


@router.get("/{recurso_id}", response_model=RecursoEducativoOut)
def obtener_recurso(recurso_id: str, db: Session = Depends(get_db)):
    recurso = db.query(RecursoEducativo).filter_by(id=recurso_id).first()
    if not recurso:
        raise HTTPException(404, "Recurso no encontrado")
    return recurso


@router.put("/{recurso_id}", response_model=RecursoEducativoOut)
def actualizar_recurso(
    recurso_id: str, datos: RecursoEducativoUpdate, db: Session = Depends(get_db)
):
    recurso = db.query(RecursoEducativo).filter_by(id=recurso_id).first()
    if not recurso:
        raise HTTPException(404, "Recurso no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(recurso, campo, valor)

    db.commit()
    db.refresh(recurso)
    return recurso


@router.post("/archivos/{recurso_id}", response_model=ArchivoRecursoOut, status_code=201)
async def subir_archivo_de_recurso(
    recurso_id: str,
    tipo_archivo: str = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if tipo_archivo not in TIPOS_PERMITIDOS:
        raise HTTPException(400, f"tipo_archivo debe ser uno de: {TIPOS_PERMITIDOS}")

    recurso = db.query(RecursoEducativo).filter_by(id=recurso_id).first()
    if not recurso:
        raise HTTPException(404, "Recurso no encontrado")

    contenido = await archivo.read()
    url = subir_archivo(contenido, archivo.filename, archivo.content_type)

    registro = ArchivoRecurso(recurso_id=recurso_id, tipo_archivo=tipo_archivo, url=url)
    db.add(registro)
    db.commit()
    db.refresh(registro)
    if tipo_archivo == "video":
        recurso.url_descarga = url
        db.commit()
    return registro


@router.get("/archivos/{recurso_id}", response_model=list[ArchivoRecursoOut])
def listar_archivos_de_recurso(recurso_id: str, db: Session = Depends(get_db)):
    return db.query(ArchivoRecurso).filter_by(recurso_id=recurso_id).all()
