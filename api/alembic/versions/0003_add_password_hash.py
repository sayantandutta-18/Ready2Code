"""add password_hash to users

Revision ID: 0003_add_password_hash
Revises: 0002_add_scene_and_starter_code
Create Date: 2026-11-08 02:35:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '0003_add_password_hash'
down_revision = '0002_add_scene_and_starter_code'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'password_hash' not in existing_columns:
        op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))

def downgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'password_hash' in existing_columns:
        op.drop_column('users', 'password_hash')
