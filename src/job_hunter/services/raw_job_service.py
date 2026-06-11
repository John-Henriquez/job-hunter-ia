from job_hunter.models.raw_job import RawJob


class RawJobService:

    def __init__(self, repository):
        self.repository = repository

    def save_raw_job(
        self,
        source,
        external_id,
        raw_payload,
    ):

        existing = self.repository.get_by_external_id(
            external_id
        )

        if existing:
            return existing

        raw_job = RawJob(
            source=source,
            external_id=external_id,
            raw_payload=raw_payload,
        )

        return self.repository.create(raw_job)