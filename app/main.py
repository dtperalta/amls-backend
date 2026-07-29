from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.modules.auth.cleanup import eliminar_cuentas_no_verificadas
from app.modules.auth.router import router as auth_router
from app.modules.content.router import router as content_router
from app.modules.ml.router import router as ml_router
from app.modules.profile.router import router as profile_router

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Corre cada 30 minutos mientras el servidor esté activo.
    scheduler.add_job(eliminar_cuentas_no_verificadas, "interval", minutes=30)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="AMLS Backend",
    description="Backend del sistema de Aprendizaje Móvil Adaptativo (AMLS).",
    version="0.1.0",
    lifespan=lifespan,
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


app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(profile_router, prefix="/profile", tags=["Perfil"])
app.include_router(content_router, prefix="/content", tags=["Contenido"])
app.include_router(ml_router, prefix="/ml", tags=["ML Recommender"])

