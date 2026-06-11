from datetime import datetime

from job_hunter.models.job import Job
from job_hunter.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(
        self,
        title: str,
        company: str = None,
        location: str = None,
        work_mode: str = None,
        salary: str = None,
        seniority: str = None,
        modality: str = None,
        category: str = None,
        description: str = None,
        source: str = None,
        url: str = None,
        published_at: datetime = None,
    ) -> Job:
        job = Job(
            title=title,
            company=company,
            location=location,
            work_mode=work_mode,
            salary=salary,
            seniority=seniority,
            modality=modality,
            category=category,
            description=description,
            source=source,
            url=url,
            published_at=published_at,
        )
        return self.repository.create_job(job)

    def list_jobs(self) -> list[Job]:
        return self.repository.get_all()

    def get_job(self, job_id: int) -> Job | None:
        return self.repository.get_by_id(job_id)

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete_job(job_id)