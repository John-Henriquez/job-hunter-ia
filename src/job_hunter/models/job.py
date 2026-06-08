from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from job_hunter.config.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

    work_mode = Column(String(50), nullable=True)  # remoto, híbrido, presencial
    salary = Column(String(100), nullable=True)

    description = Column(Text, nullable=True)

    source = Column(String(100), nullable=True)  # portal origen (linkedin, etc)
    url = Column(String(500), nullable=True)

    published_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)