from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.repositories.job_repository import JobRepository
from job_hunter.services.job_service import JobService
from job_hunter.providers.getonboard_provider import GetOnBoardProvider


def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    reporsitory = JobRepository(db)
    service = JobService(reporsitory)

    provider = GetOnBoardProvider()
    jobs_found = provider.fetch_jobs()
    print(f"Vacantes encontradas: {len(jobs_found)}")

    jobs = service.list_jobs()
    print("\nJobs en la base de datos:")

    for job in jobs:
        print(
            f"- {job.id} | {job.title} | {job.company}"
        )
    db.close()

if __name__ == "__main__":
    main()