"""add scene and starter_code to problems

Revision ID: 0002_add_scene_and_starter_code
Revises: 0001_initial_schema
Create Date: 2026-11-05 13:26:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '0002_add_scene_and_starter_code'
down_revision = '0001_initial_schema'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('problems')]
    if 'scene' not in existing_columns:
        op.add_column('problems', sa.Column('scene', sa.String(length=64), nullable=True))
    if 'starter_code' not in existing_columns:
        op.add_column('problems', sa.Column('starter_code', sa.Text(), nullable=True))

def downgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('problems')]
    if 'starter_code' in existing_columns:
        op.drop_column('problems', 'starter_code')
    if 'scene' in existing_columns:
        op.drop_column('problems', 'scene')
