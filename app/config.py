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


settings = Settings()
