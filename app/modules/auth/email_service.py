"""
Envío de correos vía la API HTTP de Resend.

Se usa HTTP (puerto 443) en vez de SMTP (puertos 25/465/587) a propósito:
varias plataformas de hosting gratuitas (Render, Vercel, etc.) bloquean
o dan soporte poco confiable a SMTP saliente, mientras que HTTPS nunca
se bloquea. Ver ARCHITECTURE.md para el detalle de esta decisión.
"""
import httpx

from app.config import settings

RESEND_API_URL = "https://api.resend.com/emails"


def enviar_correo(destinatario: str, asunto: str, cuerpo_html: str) -> None:
    respuesta = httpx.post(
        RESEND_API_URL,
        headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
        json={
            "from": settings.RESEND_FROM_EMAIL,
            "to": [destinatario],
            "subject": asunto,
            "html": cuerpo_html,
        },
        timeout=10.0,
    )
    respuesta.raise_for_status()
