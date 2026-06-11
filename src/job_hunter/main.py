from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.services.raw_job_service import RawJobService
from job_hunter.providers.registry import ProviderRegistry
from job_hunter.providers.getonboard_provider import GetOnBoardProvider



def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try: 
        registry = ProviderRegistry()
        registry.register(GetOnBoardProvider())

        repository = RawJobRepository(db)
        service = RawJobService(repository)

        total_saved  = 0
        total_skipped  = 0

        for provider in registry.get_all():
            raw_jobs = provider.fetch_jobs()
            parsed_jobs = provider.parse_jobs(raw_jobs)
            saved = 0

            for job in parsed_jobs:
                existing = repository.get_by_external_id(job["external_id"])
                if existing:
                    total_skipped += 1
                    continue
                result = service.save_raw_job(
                    source=job["source"],
                    external_id=job["external_id"],
                    raw_payload=job["raw_payload"],
                )
                saved += 1

            total_saved += saved
            print(f"[{provider.source_name}] Guardados: {saved} | Duplicados: {len(parsed_jobs) - saved}")

        print(f"\nResultados:")
        print(f"  Guardados : {total_saved}")
        print(f"  Duplicados: {total_skipped}")

    finally:
        db.close()

if __name__ == "__main__":
    main()