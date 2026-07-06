"""
Configuración de acceso a base de datos con SQLAlchemy.

Esto es Postgres "puro" — no usamos ningún SDK propietario de Supabase.
Si en la tesis cambias de proveedor, solo cambia DATABASE_URL en .env.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


def get_engine_url() -> str:
    """
    Devuelve la URL de conexión lista para SQLAlchemy.

    Supabase entrega la URL como "postgresql://...". Forzamos el driver
    "psycopg" (v3) explícitamente, para no depender de que psycopg2 esté
    instalado (más problemático de compilar en Windows).

    Se expone como función (no como variable calculada una sola vez)
    para que tanto app/main.py como alembic/env.py puedan usar
    exactamente la misma lógica sin duplicar código.
    """
    url = settings.DATABASE_URL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


engine = create_engine(get_engine_url(), pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesión de DB por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
