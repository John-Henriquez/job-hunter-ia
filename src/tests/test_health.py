from job_hunter.api.app import app, get_app_version, health


def test_health_returns_status_and_version():
    assert health() == {
        "status": "ok",
        "version": get_app_version(),
    }


def test_fastapi_version_uses_version_file():
    assert app.version == get_app_version()
