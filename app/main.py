from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(
    title="AMLS Backend",
    description="Backend del sistema de Aprendizaje Móvil Adaptativo (AMLS).",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"servicio": "AMLS Backend", "estado": "activo"}


@app.get("/health/db")
def health_db():
    """
    Verifica que la conexión a Postgres (Supabase) funciona.
    Este es el primer endpoint a probar después de configurar el .env.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "conectado"}
    except Exception as e:
        return {"database": "error", "detalle": str(e)}


from app.modules.profile.router import router as profile_router

app.include_router(profile_router, prefix="/profile", tags=["Perfil"])
# from app.modules.content.router import router as content_router
# app.include_router(content_router, prefix="/content", tags=["Contenido"])
