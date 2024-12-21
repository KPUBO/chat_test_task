from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from core.models import Base

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    foo: Mapped[int]
    bar: Mapped[int]

    __table_args__ = (UniqueConstraint( 'foo', 'bar'),)