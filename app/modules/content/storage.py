"""
Cliente de almacenamiento para Cloudflare R2 (compatible con S3).
"""
import uuid
from functools import lru_cache

import boto3

from app.config import settings


@lru_cache
def _get_client():
    """
    Cliente perezoso: se crea solo la primera vez que se necesita,
    no al importar el módulo.
    """
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def subir_archivo(contenido: bytes, nombre_original: str | None, content_type: str) -> str:
    nombre_original = nombre_original or "archivo"
    extension = nombre_original.split(".")[-1] if "." in nombre_original else "bin"
    clave = f"{uuid.uuid4()}.{extension}"

    _get_client().put_object(
        Bucket=settings.R2_BUCKET_NAME,
        Key=clave,
        Body=contenido,
        ContentType=content_type,
    )

    return f"{settings.R2_PUBLIC_URL}/{clave}"
