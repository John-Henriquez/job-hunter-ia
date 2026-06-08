from job_hunter.models.job import Job
from job_hunter.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(
        self,
        title: str,
        company: str,
        location: str,
        work_mode: str,
        salary: str,
        description: str,
        source: str,
        url: str,
    ) -> Job:

        job = Job(
            title=title,
            company=company,
            location=location,
            work_mode=work_mode,
            salary=salary,
            description=description,
            source=source,
            url=url,
        )

        return self.repository.create_job(job)

    def list_jobs(self) -> list[Job]:
        return self.repository.get_all()

    def get_job(self, job_id: int) -> Job | None:
        return self.repository.get_by_id(job_id)

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete_job(job_id)