from job_hunter.models.raw_job import RawJob


class RawJobRepository:

    def __init__(self, db):
        self.db = db

    def create(self, raw_job):
        self.db.add(raw_job)
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job

    def get_by_source_external_id(self, source, external_id):
        return (
            self.db.query(RawJob)
            .filter(RawJob.source == source)
            .filter(RawJob.external_id == external_id)
            .first()
        )

    def get_unprocessed(self):
        return (
            self.db.query(RawJob)
            .filter(RawJob.processed.is_(False))
            .all()
        )

    def mark_processed(self, raw_job):
        raw_job.processed = True
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job
