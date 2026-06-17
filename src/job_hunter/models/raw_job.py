from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from job_hunter.config.database import Base


class RawJob(Base):
    __tablename__ = "raw_jobs"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_raw_jobs_source_external_id"),
    )

    id = Column(Integer, primary_key=True)

    source = Column(String(100), nullable=False)

    external_id = Column(String(500), nullable=False)

    raw_payload = Column(JSONB, nullable=False)

    processed = Column(Boolean, default=False)

    scraped_at = Column(DateTime, default=datetime.utcnow)
