from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    s3_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Legacy column retained for schema compatibility; stores job-match score.
    ats_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    required_matched: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    required_missing: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    preferred_matched: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    preferred_missing: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    ai_analysis: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

   