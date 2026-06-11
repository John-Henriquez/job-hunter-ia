import requests
from datetime import datetime
from job_hunter.models.job import Job
from job_hunter.normalizers.base_normalizer import BaseNormalizer


class GetOnBoardNormalizer(BaseNormalizer):

    BASE_URL = "https://www.getonbrd.com/api/v0"

    def __init__(self):
        self._company_cache: dict[str, str] = {}
        self._seniority_cache: dict[str, str] = {}
        self._modality_cache: dict[str, str] = {}
        self._load_lookups()

    def _load_lookups(self):
        print("[Normalizer] Cargando lookups...")
        self._seniority_cache = self._fetch_lookup("seniorities")
        self._modality_cache = self._fetch_lookup("modalities")
        print(f"[Normalizer] Seniorities: {len(self._seniority_cache)} | Modalities: {len(self._modality_cache)}")

    def _fetch_lookup(self, endpoint: str) -> dict[str, str]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                timeout=15,
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            return {
                item["id"]: item["attributes"]["name"]
                for item in data
            }
        except requests.RequestException as e:
            print(f"[Normalizer] Error cargando {endpoint}: {e}")
            return {}

    def _get_company_name(self, company_id: str) -> str | None:
        if not company_id:
            return None

        if company_id in self._company_cache:
            return self._company_cache[company_id]

        try:
            response = requests.get(
                f"{self.BASE_URL}/companies/{company_id}",
                timeout=15,
            )
            response.raise_for_status()
            data = response.json().get("data", {})
            name = data.get("attributes", {}).get("name")
            self._company_cache[company_id] = name
            return name
        except requests.RequestException:
            return None

    def _parse_salary(self, min_salary, max_salary) -> str | None:
        if min_salary and max_salary:
            return f"{min_salary} - {max_salary}"
        if min_salary:
            return str(min_salary)
        if max_salary:
            return str(max_salary)
        return None

    def _parse_published_at(self, timestamp) -> datetime | None:
        if not timestamp:
            return None
        try:
            return datetime.fromtimestamp(int(timestamp))
        except (ValueError, TypeError):
            return None

    def normalize(self, raw_payload: dict) -> Job | None:
        try:
            attrs = raw_payload.get("attributes", {})
            links = raw_payload.get("links", {})

            title = attrs.get("title")
            if not title:
                return None

            company_id = str(
                attrs.get("company", {})
                .get("data", {})
                .get("id", "")
            )
            company_name = self._get_company_name(company_id)

            seniority_id = str(
                attrs.get("seniority", {})
                .get("data", {})
                .get("id", "")
            )
            modality_id = str(
                attrs.get("modality", {})
                .get("data", {})
                .get("id", "")
            )

            countries = attrs.get("countries", [])
            location = countries[0] if countries else None

            return Job(
                title=title,
                company=company_name,
                location=location,
                work_mode=attrs.get("remote_modality"),
                salary=self._parse_salary(
                    attrs.get("min_salary"),
                    attrs.get("max_salary"),
                ),
                seniority=self._seniority_cache.get(seniority_id),
                modality=self._modality_cache.get(modality_id),
                category=attrs.get("category_name"),
                description=attrs.get("description"),
                url=links.get("public_url"),
                published_at=self._parse_published_at(
                    attrs.get("published_at")
                ),
                source="getonboard",
            )

        except Exception as e:
            print(f"[Normalizer] Error normalizando job: {e}")
            return None