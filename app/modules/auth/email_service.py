"""
Envío de correos vía SMTP (Gmail).

Nota de diseño: esta función es intencionalmente síncrona y simple.
Se ejecuta como BackgroundTask desde los endpoints, para no bloquear
la respuesta HTTP mientras se envía el correo.
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from app.config import settings


def enviar_correo(destinatario: str, asunto: str, cuerpo_html: str) -> None:
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = formataddr((settings.SMTP_FROM_NAME, settings.SMTP_USER))
    mensaje["To"] = destinatario
    mensaje.attach(MIMEText(cuerpo_html, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, destinatario, mensaje.as_string())
