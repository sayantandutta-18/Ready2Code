"""add scene and starter_code to problems

Revision ID: 0002_add_scene_and_starter_code
Revises: 0001_initial
Create Date: 2026-11-05 13:26:00

"""
from alembic import op
import sqlalchemy as sa

revision = '0002_add_scene_and_starter_code'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('problems', sa.Column('scene', sa.String(length=64), nullable=True))
    op.add_column('problems', sa.Column('starter_code', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('problems', 'starter_code')
    op.drop_column('problems', 'scene')
