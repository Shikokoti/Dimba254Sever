"""add logo_url to team

Revision ID: b1c2d3e4f5a6
Revises: ac819a617c66
Create Date: 2026-05-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b1c2d3e4f5a6'
down_revision = 'ac819a617c66'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('team', sa.Column('logo_url', sa.String(length=500), nullable=True))


def downgrade():
    op.drop_column('team', 'logo_url')
