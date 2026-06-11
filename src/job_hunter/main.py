from job_hunter.config.database import engine, SessionLocal, Base
from job_hunter.models.job import Job
from job_hunter.models.raw_job import RawJob
from job_hunter.providers.registry import ProviderRegistry
from job_hunter.providers.getonboard_provider import GetOnBoardProvider
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.repositories.job_repository import JobRepository
from job_hunter.services.fetch_service import FetchService
from job_hunter.normalizers.getonboard_normalizer import GetOnBoardNormalizer



def main():
    print(" Job Hunter AI iniciado...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try: 
        registry = ProviderRegistry()
        registry.register(GetOnBoardProvider())

        raw_repository = RawJobRepository(db)
        job_repository = JobRepository(db)
        normalizer = GetOnBoardNormalizer()

        fetch_service = FetchService(
            registry=registry,
            raw_repository=raw_repository,
            job_repository=job_repository,
            normalizer=normalizer,
        )
        fetch_service.run()

    finally:
        db.close()

if __name__ == "__main__":
    main()