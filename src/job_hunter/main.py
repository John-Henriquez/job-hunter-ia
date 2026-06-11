from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.services.raw_job_service import RawJobService
from job_hunter.providers.getonboard_provider import GetOnBoardProvider



def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try: 
        repository = RawJobRepository(db)
        service = RawJobService(repository)
        provider = GetOnBoardProvider()

        raw_jobs = provider.fetch_jobs()
        parsed_jobs= provider.parse_jobs(raw_jobs)

        saved = 0
        skipped = 0

        for job in parsed_jobs:
            result = service.save_raw_job(
                source=job["source"],
                external_id=job["external_id"],
                raw_payload=job["raw_payload"],
            )
            if result.scraped_at and result.external_id == job["external_id"]:
                saved += 1

        skipped = len(parsed_jobs) - saved

        print(f"\nResultados:")
        print(f"  Guardados : {saved}")
        print(f"  Duplicados: {skipped}")

    finally:
        db.close()

if __name__ == "__main__":
    main()