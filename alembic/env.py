import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import create_engine, pool

from alembic import context

# Permite importar "app.*" al correr alembic desde la raíz del proyecto
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import Base, get_engine_url  # noqa: E402

# Importa aquí los modelos de cada módulo a medida que se agreguen,
# para que Alembic los detecte en el "autogenerate":
from app.modules.profile.models import PerfilAprendiz
# from app.modules.content.models import RecursoEducativo

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# IMPORTANTE: no usamos config.set_main_option("sqlalchemy.url", ...)
# porque Alembic guarda esa opción en un ConfigParser normal, el cual
# interpreta el símbolo "%" como sintaxis de interpolación. Si la
# contraseña de la base de datos tiene "%" (por caracteres especiales
# codificados en la URL), eso rompe con un ValueError.
# En vez de eso, guardamos la URL en una variable Python normal y la
# usamos directamente donde se necesita.
DB_URL = get_engine_url()

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DB_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
