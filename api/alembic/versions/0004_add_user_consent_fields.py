"""add user consent fields terms_accepted_at and terms_version

Revision ID: 0004_add_user_consent_fields
Revises: 0003_add_password_hash
Create Date: 2026-11-11 20:30:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = '0004_add_user_consent_fields'
down_revision = '0003_add_password_hash'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'terms_accepted_at' not in existing_columns:
        op.add_column('users', sa.Column('terms_accepted_at', sa.DateTime(timezone=True), nullable=True))
    if 'terms_version' not in existing_columns:
        op.add_column('users', sa.Column('terms_version', sa.String(length=32), nullable=True))

def downgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'terms_version' in existing_columns:
        op.drop_column('users', 'terms_version')
    if 'terms_accepted_at' in existing_columns:
        op.drop_column('users', 'terms_accepted_at')
