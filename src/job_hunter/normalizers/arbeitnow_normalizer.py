from datetime import datetime
from job_hunter.models.job import Job
from job_hunter.normalizers.base_normalizer import BaseNormalizer


class ArbeitnowNormalizer(BaseNormalizer):

    def _parse_published_at(self, timestamp) -> datetime | None:
        if not timestamp:
            return None
        try:
            return datetime.fromtimestamp(int(timestamp))
        except (ValueError, TypeError):
            return None

    def _parse_work_mode(self, remote: bool) -> str:
        return "remote" if remote else "on-site"

    def normalize(self, raw_payload: dict) -> Job | None:
        try:
            title = raw_payload.get("title")
            if not title:
                return None

            tags = raw_payload.get("tags", [])
            job_types = raw_payload.get("job_types", [])

            return Job(
                title=title,
                company=raw_payload.get("company_name"),
                location=raw_payload.get("location"),
                work_mode=self._parse_work_mode(
                    raw_payload.get("remote", False)
                ),
                salary=None,
                seniority=None,
                modality=job_types[0] if job_types else None,
                category=tags[0] if tags else None,
                description=raw_payload.get("description"),
                url=raw_payload.get("url"),
                published_at=self._parse_published_at(
                    raw_payload.get("created_at")
                ),
                source="arbeitnow",
            )

        except Exception as e:
            print(f"[ArbeitnowNormalizer] Error: {e}")
            return None