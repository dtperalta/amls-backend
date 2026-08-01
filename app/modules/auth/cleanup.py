"""
Limpieza automática de cuentas no verificadas.

Corre periódicamente (ver app/main.py) para borrar usuarios que nunca
verificaron su correo dentro de la ventana de tiempo permitida.
"""
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.database import SessionLocal
from app.modules.auth.models import Usuario


def eliminar_cuentas_no_verificadas() -> None:
    db = SessionLocal()
    try:
        limite = datetime.now(timezone.utc) - timedelta(
            hours=settings.HORAS_EXPIRACION_VERIFICACION
        )
        eliminadas = (
            db.query(Usuario)
            .filter(Usuario.email_verificado.is_(False), Usuario.created_at < limite)
            .delete(synchronize_session=False)
        )
        db.commit()
        if eliminadas:
            print(f"[cleanup] Se eliminaron {eliminadas} cuenta(s) no verificada(s).")
    finally:
        db.close()
