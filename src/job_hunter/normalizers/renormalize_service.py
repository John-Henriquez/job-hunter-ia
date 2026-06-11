from datetime import datetime
from job_hunter.repositories.raw_job_repository import RawJobRepository
from job_hunter.repositories.job_repository import JobRepository

WORK_MODE_MAP = {
    "fully_remote": "remote",
    "remote_local": "remote",
    "no_remote": "on-site",
    "hybrid": "hybrid",
    "remote": "remote",
    "on-site": "on-site",
}


class RenormalizeService:

    def __init__(self, raw_repository: RawJobRepository, job_repository: JobRepository):
        self.raw_repository = raw_repository
        self.job_repository = job_repository

    def _parse_timestamp(self, value) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromtimestamp(int(value))
        except (ValueError, TypeError):
            return None

    def _fix_getonboard(self, job, raw_payload):
        attrs = raw_payload.get("attributes", {})
        job.published_at = self._parse_timestamp(attrs.get("published_at"))
        job.work_mode = WORK_MODE_MAP.get(job.work_mode, job.work_mode)

    def _fix_arbeitnow(self, job, raw_payload):
        job.published_at = self._parse_timestamp(raw_payload.get("created_at"))
        job.work_mode = WORK_MODE_MAP.get(job.work_mode, job.work_mode)

    def run(self) -> dict:
        print("[Renormalize] Iniciando re-normalización...")

        jobs = self.job_repository.get_all()
        fixed = 0
        failed = 0

        for job in jobs:
            try:
                raw = self.raw_repository.get_by_external_id(
                    self._get_external_id(job)
                )
                if not raw:
                    failed += 1
                    continue

                if job.source == "getonboard":
                    self._fix_getonboard(job, raw.raw_payload)
                elif job.source == "arbeitnow":
                    self._fix_arbeitnow(job, raw.raw_payload)

                job.work_mode = WORK_MODE_MAP.get(job.work_mode, job.work_mode)
                fixed += 1

            except Exception as e:
                print(f"[Renormalize] Error en job {job.id}: {e}")
                failed += 1

        self.job_repository.db.commit()

        print(f"[Renormalize] Corregidos: {fixed} | Fallos: {failed}")
        return {"fixed": fixed, "failed": failed}

    def _get_external_id(self, job) -> str:
        from job_hunter.models.raw_job import RawJob
        raw = (
            self.raw_repository.db.query(RawJob)
            .filter(RawJob.source == job.source)
            .filter(RawJob.raw_payload["title"].astext == job.title)
            .first()
        )
        return raw.external_id if raw else ""