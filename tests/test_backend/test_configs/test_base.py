import pytest
from pydantic import ValidationError
from nazi_symbols_classification_backend.app.configs.base import Settings
from nazi_symbols_classification_backend.app.configs import get_settings


@pytest.mark.parametrize("mode, settings_cls",
                         [("DEV", Settings),
                          ("TEST", Settings),
                          ("PROD", Settings),
                          (None, Settings),
                          ("None", Settings)])
def test_get_settings(monkeypatch, mode, settings_cls):
    if mode:
        monkeypatch.setenv("MODE", mode)
    settings = get_settings()
    # assert the settings is an instance of the corresponding settings class
    assert isinstance(settings, settings_cls)
    if mode:
        monkeypatch.delenv("MODE")


@pytest.mark.parametrize("cors_origins, expected_result",
                         [(["https://allianz.com", "https://allianz.de"],
                           ["https://allianz.com", "https://allianz.de"]),
                          ("https://allianz.com, https://allianz.de",
                           ["https://allianz.com", "https://allianz.de"]),
                          ("['https://allianz.com', 'https://allianz.de']",
                           ["https://allianz.com", "https://allianz.de"])
                          ])
def test_assemble_cors_origins_success(cors_origins, expected_result):
    s = Settings(CORS_ORIGINS=cors_origins)
    assert s.CORS_ORIGINS == expected_result


def test_assemble_cors_origins_fail():
    with pytest.raises(ValueError) as e:
        Settings(CORS_ORIGINS=None)
    assert type(e.value) == ValidationError
    assert len(e.value.errors()) == 1
    assert e.value.errors()[0]["msg"] == 'Value error, None'

