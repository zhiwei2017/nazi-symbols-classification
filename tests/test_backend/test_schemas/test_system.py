from nazi_symbols_classification_backend.app.schemas.system import HealthResponse, VersionResponse


def test_healthresponse():
    hr = HealthResponse(message="Hello World")
    assert hr.message == "Hello World"


def test_versionresponse():
    vr = VersionResponse(version="1.0.0")
    assert vr.version == "1.0.0"
