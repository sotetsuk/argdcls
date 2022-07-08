from dataclasses import dataclass

import pytest

import argdcls
from argdcls.config import _parse


@dataclass
class Config:
    lr: float
    adam: bool = False


def test_load_params():
    # "@"
    config = argdcls.load(Config, ["@lr=1.0"])
    assert config.lr == 1.0

    # ""
    config = argdcls.load(Config, ["lr=1.0", "adam=True"])
    assert config.lr == 1.0
    assert config.adam


def test_error_cases():
    # raise value error if typo exists
    with pytest.raises(Exception) as e:
        _ = argdcls.load(Config, ["lr=1.0", "adm=True"])
    assert str(e.value) == "Parameter \"adm\" is not in the dataclass fields: ['lr', 'adam']."

    # avoid overriding
    with pytest.raises(Exception) as e:
        _ = argdcls.load(Config, ["@adam=True"])
    assert (
        str(e.value)
        == 'Parameter "adam" must have no default value but have default value: "False". You may use "adam=True" instead.'
    )


def test_parse():
    # "@"
    param_t, key, val = _parse("@lr=1.0")
    assert param_t == "@"
    assert key == "lr"
    assert val == 1.0

    # ""
    param_t, key, val = _parse("lr=1.0")
    assert param_t == ""
    assert key == "lr"
    assert val == 1.0
