from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from job_hunter.repositories.job_repository import JobRepository


def test_update_application_status_updates_existing_job():
    db = MagicMock()
    repository = JobRepository(db)
    job = SimpleNamespace(id=1, application_status="saved")
    repository.get_by_id = MagicMock(return_value=job)

    result = repository.update_application_status(1, "applied")

    assert result is job
    assert job.application_status == "applied"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(job)


def test_update_application_status_returns_none_for_missing_job():
    db = MagicMock()
    repository = JobRepository(db)
    repository.get_by_id = MagicMock(return_value=None)

    result = repository.update_application_status(1, "discarded")

    assert result is None
    db.commit.assert_not_called()
    db.refresh.assert_not_called()


def test_update_application_status_rejects_invalid_status():
    repository = JobRepository(MagicMock())

    with pytest.raises(ValueError):
        repository.update_application_status(1, "maybe")
