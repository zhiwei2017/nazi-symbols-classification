import importlib.metadata


def test_version():
    assert isinstance(importlib.metadata.version("nazi_symbols_classification"), str)
