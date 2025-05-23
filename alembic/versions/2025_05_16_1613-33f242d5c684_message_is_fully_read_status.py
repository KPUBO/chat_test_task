"""message is_fully_read status

Revision ID: 33f242d5c684
Revises: 529e42e5a46e
Create Date: 2025-05-16 16:13:56.569083

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "33f242d5c684"
down_revision: Union[str, None] = "529e42e5a46e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages", sa.Column("is_fully_read", sa.Boolean(), nullable=False, server_default='false')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("messages", "is_fully_read")
    # ### end Alembic commands ###
