from datetime import datetime, timedelta, timezone

from app.config import settings
from app.database import SessionLocal
from app.modules.auth.models import Usuario


def eliminar_cuentas_no_verificadas() -> None:
    ahora = datetime.now(timezone.utc)
    print(f"[cleanup] Ejecutando revisión de cuentas no verificadas — {ahora.isoformat()}")

    db = SessionLocal()
    try:
        limite = ahora - timedelta(hours=settings.HORAS_EXPIRACION_VERIFICACION)
        eliminadas = (
            db.query(Usuario)
            .filter(Usuario.email_verificado.is_(False), Usuario.created_at < limite)
            .delete(synchronize_session=False)
        )
        db.commit()
        print(f"[cleanup] Resultado: {eliminadas} cuenta(s) eliminada(s).")
    except Exception as e:
        print(f"[cleanup] ERROR durante la limpieza: {e}")
    finally:
        db.close()
