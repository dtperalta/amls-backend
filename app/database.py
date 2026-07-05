"""
Configuración de acceso a base de datos con SQLAlchemy.

Esto es Postgres "puro" — no usamos ningún SDK propietario de Supabase.
Si en la tesis cambias de proveedor, solo cambia DATABASE_URL en .env.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesión de DB por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
