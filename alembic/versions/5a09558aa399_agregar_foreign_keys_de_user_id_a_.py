"""agregar foreign keys de user_id a usuarios

Revision ID: 5a09558aa399
Revises: 2113e6a84a49
Create Date: 2026-07-09 21:50:14.193093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5a09558aa399'
down_revision: Union[str, Sequence[str], None] = '2113e6a84a49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # La tabla perfil_aprendiz fue recreada manualmente fuera de Alembic
    # y quedó con un nombre de columna corrupto y sin la restricción
    # UNIQUE. Se reconstruye aquí desde cero, en línea con lo que
    # models.py siempre esperó, para volver a tener una única fuente
    # de verdad versionada.
    op.drop_table('perfil_aprendiz')

    op.create_table(
        'perfil_aprendiz',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('grado_perdida_auditiva', sa.String(), nullable=False, server_default='Leve'),
        sa.Column('preferencia_comunicativa', sa.String(), nullable=False, server_default='Subtítulos'),
        sa.Column('nivel_lectura', sa.String(), nullable=False, server_default='Básico'),
        sa.Column('requiere_alto_contraste', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('tamano_subtitulos', sa.Integer(), nullable=False, server_default='18'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_perfil_aprendiz_user_id'), 'perfil_aprendiz', ['user_id'], unique=True
    )

    op.create_foreign_key(
        "fk_perfil_aprendiz_user_id_usuarios",
        "perfil_aprendiz", "usuarios", ["user_id"], ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_historial_interacciones_user_id_usuarios",
        "historial_interacciones", "usuarios", ["user_id"], ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_historial_interacciones_user_id_usuarios",
        "historial_interacciones", type_="foreignkey",
    )
    op.drop_constraint(
        "fk_perfil_aprendiz_user_id_usuarios",
        "perfil_aprendiz", type_="foreignkey",
    )
    op.drop_table('perfil_aprendiz')