from sqlalchemy import Boolean, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from lichenid.database.mixins.id_mixins import IDMixin
from lichenid.database.mixins.timestamp_mixins import TimestampsMixin
from lichenid.database.models.base import Base


class User(Base, IDMixin, TimestampsMixin):
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)



