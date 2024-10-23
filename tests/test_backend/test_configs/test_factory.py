import pytest

from nazi_symbols_classification_backend.app.configs.base import Settings
from nazi_symbols_classification_backend.app.configs.settings_factory import SettingsFactory

def test_factory():

    factory = SettingsFactory()
    assert factory.modes() == []

    with pytest.raises(ValueError):
        factory["mode"]

    factory.register("DEV", Settings)
    factory.register("PROD", Settings, DEBUG=False)

    assert len(factory.modes()) == 2
    assert "DEV" in factory.modes()
    assert "PROD" in factory.modes()

    prod = factory["PROD"]
    assert type(prod) == Settings
    assert not prod.DEBUG

    dev = factory["DEV"]
    assert type(dev) == Settings
    assert dev.DEBUG

