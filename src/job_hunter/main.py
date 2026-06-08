from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.repositories.job_repository import JobRepository
from job_hunter.services.job_service import JobService


def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    reporsitory = JobRepository(db)
    service = JobService(reporsitory)

    job = service.create_job(
        title="Python Developer Junior",
        company="Demo Company",
        location="Chile",
        work_mode="remote",
        salary="$1.200.000",
        description="Vacante de prueba",
        source="manual",
        url="https://example.com/job",
    )
    print(f"Job insertado en: {job.id}")

    jobs = service.list_jobs()
    print("\nJobs en la base de datos:")

    for job in jobs:
        print(
            f"- {job.id} | {job.title} | {job.company}"
        )
    db.close()

if __name__ == "__main__":
    main()