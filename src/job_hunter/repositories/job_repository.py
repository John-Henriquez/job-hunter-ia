from sqlalchemy.orm import Session
from sqlalchemy import or_
from job_hunter.models.job import Job

APPLICATION_STATUSES = {"saved", "applied", "interviewing", "discarded"}

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
    
    def search(
        self,
        source: str = None,
        category: str = None,
        seniority: str = None,
        modality: str = None,
        application_status: str = None,
        work_mode: str = None,
        search: str = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Job], int]:
        query = self.db.query(Job)

        if source:
            query = query.filter(Job.source == source)
        if category:
            query = query.filter(Job.category == category)
        if seniority:
            query = query.filter(Job.seniority == seniority)
        if modality:
            query = query.filter(Job.modality == modality)
        if work_mode:
            query = query.filter(Job.work_mode == work_mode)
        if application_status:
            query = query.filter(Job.application_status == application_status)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Job.title.ilike(pattern),
                    Job.company.ilike(pattern),
                )
            )

        total = query.count()

        results = (
            query
            .order_by(Job.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return results, total

    def update_application_status(self, job_id: int, status: str) -> Job | None:
        if status not in APPLICATION_STATUSES:
            raise ValueError(f"Invalid application status: {status}")

        job = self.get_by_id(job_id)
        if not job:
            return None

        job.application_status = status
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete_job(self, job_id: int) -> bool:
        job = self.get_by_id(job_id)
        if not job:
            return False
        self.db.delete(job)
        self.db.commit()
        return True
