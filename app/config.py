"""
Configuración centralizada del backend AMLS.

Principio de diseño: NINGÚN valor sensible o dependiente del entorno
(URLs, credenciales, flags) se escribe directamente en el código.
Todo se lee desde variables de entorno (archivo .env en local,
variables de entorno reales en Render/producción).

Esto es lo que te permite, en la tesis, mover este mismo código de
Supabase a otro Postgres (AWS RDS, un VPS, etc.) cambiando solo
el valor de DATABASE_URL, sin tocar una sola línea de app/.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    APP_ENV: str = "local"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    HORAS_EXPIRACION_VERIFICACION: float = 0.05
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str = "onboarding@resend.dev"
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_PUBLIC_URL: str


settings = Settings()
