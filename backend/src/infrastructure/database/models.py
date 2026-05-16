import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PasswordAnalysisModel(Base):
    __tablename__ = "password_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    entropy_bits: Mapped[float] = mapped_column(Float, nullable=False)
    pool_size: Mapped[int] = mapped_column(Integer, nullable=False)
    has_lowercase: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_uppercase: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_digits: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_symbols: Mapped[bool] = mapped_column(Boolean, nullable=False)
    strength_label: Mapped[str] = mapped_column(String(50), nullable=False)
    strength_color: Mapped[str] = mapped_column(String(20), nullable=False)