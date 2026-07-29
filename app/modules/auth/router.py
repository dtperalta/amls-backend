import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.auth.email_service import enviar_correo
from app.modules.auth.models import CodigoVerificacion, Usuario
from app.modules.auth.schemas import (
    RestablecerPasswordRequest,
    SolicitarRecuperacionRequest,
    Token,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioOut,
    VerificarCodigoRequest,
)
from app.modules.auth.security import (
    crear_access_token,
    generar_codigo_verificacion,
    hashear_password,
    verificar_password,
)

router = APIRouter()

CODIGO_EXPIRACION_MINUTOS = 15


def _crear_y_enviar_codigo(
    db: Session, usuario: Usuario, tipo: str, background_tasks: BackgroundTasks
) -> None:
    codigo = generar_codigo_verificacion()
    registro = CodigoVerificacion(
        user_id=usuario.id,
        codigo=codigo,
        tipo=tipo,
        expira_en=datetime.now(timezone.utc) + timedelta(minutes=CODIGO_EXPIRACION_MINUTOS),
    )
    db.add(registro)
    db.commit()

    if tipo == "verificacion_email":
        asunto = "Verifica tu correo - AMLS"
    else:
        asunto = "Recupera tu contraseña - AMLS"

    cuerpo = f"""
    <p>Hola {usuario.nombre_completo},</p>
    <p>Tu código es: <strong style="font-size: 24px;">{codigo}</strong></p>
    <p>Expira en {CODIGO_EXPIRACION_MINUTOS} minutos.</p>
    """
    background_tasks.add_task(enviar_correo, usuario.email, asunto, cuerpo)


@router.post("/register", response_model=UsuarioOut, status_code=201)
def registrar(
    datos: UsuarioCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    existente = db.query(Usuario).filter_by(email=datos.email).first()
    if existente:
        raise HTTPException(400, "Ya existe una cuenta con ese email")

    usuario = Usuario(
        nombre_completo=datos.nombre_completo,
        email=datos.email,
        password_hash=hashear_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    _crear_y_enviar_codigo(db, usuario, "verificacion_email", background_tasks)

    return usuario


@router.post("/login", response_model=Token)
def iniciar_sesion(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=datos.email).first()
    if not usuario or not verificar_password(datos.password, usuario.password_hash):
        raise HTTPException(401, "Email o contraseña incorrectos")

    token = crear_access_token(usuario.id)
    return Token(access_token=token, email_verificado=usuario.email_verificado)


@router.get("/me", response_model=UsuarioOut)
def obtener_usuario_actual(
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    usuario = db.query(Usuario).filter_by(id=current_user_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    return usuario


@router.post("/verificar-email")
def verificar_email(
    datos: VerificarCodigoRequest,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    registro = (
        db.query(CodigoVerificacion)
        .filter_by(
            user_id=current_user_id,
            codigo=datos.codigo,
            tipo="verificacion_email",
            usado=False,
        )
        .order_by(CodigoVerificacion.created_at.desc())
        .first()
    )
    if not registro or registro.expira_en < datetime.now(timezone.utc):
        raise HTTPException(400, "Código inválido o expirado")

    registro.usado = True
    usuario = db.query(Usuario).filter_by(id=current_user_id).first()
    usuario.email_verificado = True
    db.commit()
    return {"mensaje": "Correo verificado correctamente"}


@router.post("/reenviar-verificacion")
def reenviar_verificacion(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    usuario = db.query(Usuario).filter_by(id=current_user_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    if usuario.email_verificado:
        return {"mensaje": "Tu correo ya está verificado"}

    _crear_y_enviar_codigo(db, usuario, "verificacion_email", background_tasks)
    return {"mensaje": "Código reenviado, revisa tu correo"}


@router.post("/solicitar-recuperacion")
def solicitar_recuperacion(
    datos: SolicitarRecuperacionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter_by(email=datos.email).first()
    if usuario:
        _crear_y_enviar_codigo(db, usuario, "recuperacion_password", background_tasks)

    # Respuesta genérica siempre, exista o no el correo — evita revelar
    # a un atacante si un email está registrado en el sistema.
    return {"mensaje": "Si el correo existe, se envió un código de recuperación"}


@router.post("/restablecer-password")
def restablecer_password(datos: RestablecerPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter_by(email=datos.email).first()
    if not usuario:
        raise HTTPException(400, "Código inválido o expirado")

    registro = (
        db.query(CodigoVerificacion)
        .filter_by(
            user_id=usuario.id,
            codigo=datos.codigo,
            tipo="recuperacion_password",
            usado=False,
        )
        .order_by(CodigoVerificacion.created_at.desc())
        .first()
    )
    if not registro or registro.expira_en < datetime.now(timezone.utc):
        raise HTTPException(400, "Código inválido o expirado")

    registro.usado = True
    usuario.password_hash = hashear_password(datos.nueva_password)
    db.commit()
    return {"mensaje": "Contraseña restablecida correctamente"}
