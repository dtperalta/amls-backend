import uuid

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.security import decodificar_token

bearer_scheme = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> uuid.UUID:
    """
    Extrae y valida el user_id del JWT enviado en el header
    Authorization: Bearer <token>.

    Al usarse como dependencia, FastAPI automáticamente agrega el botón
    "Authorize" en /docs para poder probar endpoints protegidos ahí.
    """
    try:
        return decodificar_token(credentials.credentials)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        raise HTTPException(401, "Token inválido o expirado")


def get_current_verified_user_id(
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
) -> uuid.UUID:
    """
    Dependencia que extiende get_current_user_id verificando además
    que el usuario haya confirmado su correo electrónico.
    Lanza HTTP 403 si el email no está verificado.
    """
    from app.modules.auth.models import Usuario

    usuario = db.query(Usuario).filter_by(id=current_user_id).first()
    if not usuario or not usuario.email_verificado:
        raise HTTPException(403, "Debes verificar tu correo antes de continuar")
    return current_user_id
