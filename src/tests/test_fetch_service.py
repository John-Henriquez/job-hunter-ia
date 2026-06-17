from types import SimpleNamespace
from unittest.mock import MagicMock

from job_hunter.services.fetch_service import FetchService


def _provider(normalizer):
    provider = MagicMock()
    provider.source_name = "getonboard"
    provider.get_normalizer.return_value = normalizer
    provider.fetch_jobs.return_value = [{"id": "123"}]
    provider.parse_jobs.return_value = [
        {
            "source": "getonboard",
            "external_id": "123",
            "raw_payload": {"title": "Dev"},
        }
    ]
    return provider


def _normalized_job():
    return SimpleNamespace(
        title="Dev",
        company="Acme",
        location="Remote",
        work_mode="remote",
        salary=None,
        seniority=None,
        modality=None,
        category=None,
        description=None,
        source="getonboard",
        url="https://example.com/jobs/123",
        published_at=None,
    )


def test_run_skips_already_processed_raw_job():
    normalizer = MagicMock()
    provider = _provider(normalizer)
    registry = MagicMock()
    registry.get_all.return_value = [provider]
    raw_repository = MagicMock()
    raw_repository.get_by_source_external_id.return_value = SimpleNamespace(
        processed=True,
        raw_payload={"title": "Dev"},
    )
    job_repository = MagicMock()

    result = FetchService(registry, raw_repository, job_repository).run()

    assert result["skipped"] == 1
    assert result["normalized"] == 0
    normalizer.normalize.assert_not_called()
    job_repository.create_job.assert_not_called()
    raw_repository.mark_processed.assert_not_called()


def test_run_retries_existing_unprocessed_raw_job():
    normalizer = MagicMock()
    normalizer.normalize.return_value = _normalized_job()
    provider = _provider(normalizer)
    registry = MagicMock()
    registry.get_all.return_value = [provider]
    raw_job = SimpleNamespace(processed=False, raw_payload={"title": "Dev"})
    raw_repository = MagicMock()
    raw_repository.get_by_source_external_id.return_value = raw_job
    job_repository = MagicMock()

    result = FetchService(registry, raw_repository, job_repository).run()

    assert result["saved"] == 0
    assert result["normalized"] == 1
    normalizer.normalize.assert_called_once_with({"title": "Dev"})
    job_repository.create_job.assert_called_once()
    raw_repository.mark_processed.assert_called_once_with(raw_job)


def test_run_saves_and_marks_new_raw_job_after_normalization():
    normalizer = MagicMock()
    normalizer.normalize.return_value = _normalized_job()
    provider = _provider(normalizer)
    registry = MagicMock()
    registry.get_all.return_value = [provider]
    raw_job = SimpleNamespace(processed=False, raw_payload={"title": "Dev"})
    raw_repository = MagicMock()
    raw_repository.get_by_source_external_id.return_value = None
    raw_repository.create.return_value = raw_job
    job_repository = MagicMock()

    result = FetchService(registry, raw_repository, job_repository).run()

    assert result["saved"] == 1
    assert result["normalized"] == 1
    raw_repository.create.assert_called_once()
    raw_repository.mark_processed.assert_called_once_with(raw_job)
