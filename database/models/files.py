from sqlalchemy import Boolean, Text, String, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from lichenid.database.mixins.id_mixins import IDMixin
from lichenid.database.mixins.timestamp_mixins import TimestampsMixin, CreatedAtMixin
from lichenid.database.models.base import Base


class Files(Base, IDMixin, CreatedAtMixin):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'object_name', name='unique_user_object'),
    )
    object_name: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    s3_key: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    content_type: Mapped[str] = mapped_column(Text, unique=False, nullable=False)



