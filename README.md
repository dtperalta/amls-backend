# AMLS Backend

Backend del sistema de Aprendizaje Móvil Adaptativo. Ver `ARCHITECTURE.md`
para el mapeo con la propuesta original y las decisiones de diseño.

## Configuración local (primera vez)

1. **Crear entorno virtual e instalar dependencias:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   ```
   Abre `.env` y pega tu cadena de conexión real de Supabase
   (pestaña **Session pooler**, con tu password real).
   Este archivo NUNCA se sube a git (ya está en `.gitignore`).

3. **Levantar el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Verificar que todo conecta:**
   Abre en el navegador: http://127.0.0.1:8000/health/db

   Deberías ver: `{"database": "conectado"}`

   Si ves un error, revisa que:
   - Copiaste la cadena de la pestaña **Session pooler** (no Direct connection).
   - Reemplazaste `[YOUR-PASSWORD]` con tu password real.
   - No hay espacios extra al copiar/pegar en el `.env`.

5. **Documentación interactiva de la API** (autogenerada por FastAPI):
   http://127.0.0.1:8000/docs

## Siguiente paso: primera migración

Una vez que `/health/db` responda "conectado", seguimos con la primera
tabla (perfil del aprendiz) y su migración de Alembic.
