import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    nombre_completo: str
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nombre_completo: str
    email: str
    email_verificado: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email_verificado: bool


class VerificarCodigoRequest(BaseModel):
    codigo: str


class SolicitarRecuperacionRequest(BaseModel):
    email: EmailStr


class RestablecerPasswordRequest(BaseModel):
    email: EmailStr
    codigo: str
    nueva_password: str
