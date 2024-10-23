from nazi_symbols_classification_backend.app.version import __version__


def test_get_health(test_client):
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is healthy!"}


def test_get_version(test_client):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}
