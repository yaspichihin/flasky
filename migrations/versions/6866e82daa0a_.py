"""empty message

Revision ID: 6866e82daa0a
Revises: 5f85f4160724
Create Date: 2023-06-07 14:07:22.532664

"""
from sqlalchemy.orm.session import Session
from app.models import User

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6866e82daa0a'
down_revision = '5f85f4160724'
branch_labels = None
depends_on = None


def upgrade():
    session = Session(bind=op.get_bind())
    print(session.query(User).all())


def downgrade():
    pass
