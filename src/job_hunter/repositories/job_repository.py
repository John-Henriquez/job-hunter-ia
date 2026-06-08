from sqlalchemy.orm import Session
from job_hunter.models.job import Job

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job: Job) -> Job:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_all(self) -> list[Job]:
        return self.db.query(Job).all()
    
    def get_by_id(self, job_id: int) -> Job | None:
        return (
            self.db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def delete_job(self, job_id: int) -> bool:
        job = self.get_by_id(job_id)
        if not job:
            return False
        self.db.delete(job)
        self.db.commit()
        return True