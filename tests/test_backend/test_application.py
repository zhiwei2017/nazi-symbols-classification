import unittest.mock as mock
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from nazi_symbols_classification_backend.app.application import create_application
from nazi_symbols_classification_backend.app.configs import Settings


def test_create_application():
    app = create_application()
    assert isinstance(app, FastAPI)


@mock.patch("nazi_symbols_classification_backend.app.application.get_settings")
def test_create_application_with_cors_origins(mocked_get_settings):
    mocked_get_settings.return_value = Settings(CORS_ORIGINS="https://allianz.com, https://allianz.de")
    app = create_application()
    assert isinstance(app, FastAPI)
    for m in app.user_middleware:
        if isinstance(m, CORSMiddleware):
            assert m.options == {'allow_origins': ['https://allianz.com', 'https://allianz.de'],
                                 'allow_origin_regex': 'https:\\/\\/.*\\.allianz\\.?',
                                 'allow_credentials': True,
                                 'allow_methods': ['GET'],
                                 'allow_headers': []}
