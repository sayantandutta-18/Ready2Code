"""initial schema

Revision ID: 0001_initial_schema
Revises: None
Create Date: 2026-11-08 02:00:00

"""
from alembic import op
import sqlalchemy as sa
from app.models.entities import Base

revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
