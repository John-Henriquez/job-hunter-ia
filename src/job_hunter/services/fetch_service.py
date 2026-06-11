from job_hunter.providers.registry import ProviderRegistry
from job_hunter.services.raw_job_service import RawJobService
from job_hunter.services.job_service import JobService
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.repositories.job_repository import JobRepository


class FetchService:

    def __init__(
        self,
        registry: ProviderRegistry,
        raw_repository: RawJobRepository,
        job_repository: JobRepository,
    ):
        self.registry = registry
        self.raw_service = RawJobService(raw_repository)
        self.job_service = JobService(job_repository)
        self.raw_repository = raw_repository

    def run(self) -> dict:
        total_saved = 0
        total_skipped = 0
        total_normalized = 0
        total_failed = 0

        for provider in self.registry.get_all():
            print(f"\n[{provider.source_name}] Iniciando fetch...")
            normalizer = provider.get_normalizer()

            raw_jobs = provider.fetch_jobs()
            parsed_jobs = provider.parse_jobs(raw_jobs)
            saved = 0

            for job in parsed_jobs:
                existing = self.raw_repository.get_by_external_id(
                    job["external_id"]
                )
                if existing:
                    total_skipped += 1
                    continue

                raw_job = self.raw_service.save_raw_job(
                    source=job["source"],
                    external_id=job["external_id"],
                    raw_payload=job["raw_payload"],
                )
                saved += 1

                normalized = normalizer.normalize(job["raw_payload"])
                if normalized:
                    self.job_service.create_job(
                        title=normalized.title,
                        company=normalized.company,
                        location=normalized.location,
                        work_mode=normalized.work_mode,
                        salary=normalized.salary,
                        seniority=normalized.seniority,
                        modality=normalized.modality,
                        category=normalized.category,
                        description=normalized.description,
                        source=normalized.source,
                        url=normalized.url,
                    )
                    total_normalized += 1
                else:
                    total_failed += 1

            total_saved += saved
            print(f"[{provider.source_name}] Guardados: {saved} | Duplicados: {len(parsed_jobs) - saved}")

        print(f"\nResumen total:")
        print(f"  Raw guardados  : {total_saved}")
        print(f"  Duplicados     : {total_skipped}")
        print(f"  Normalizados   : {total_normalized}")
        print(f"  Fallos         : {total_failed}")

        return {
            "saved": total_saved,
            "skipped": total_skipped,
            "normalized": total_normalized,
            "failed": total_failed,
        }