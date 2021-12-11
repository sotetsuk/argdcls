from dataclasses import dataclass

import argdcls
from argdcls.config import _parse


@dataclass
class Config:
    lr: float
    adam: bool = False


def test_load_params():
    # "*"
    config = argdcls.load(Config, ["@lr=1.0"])
    assert config.lr == 1.0

    # ""
    config = argdcls.load(Config, ["lr=1.0", "adam=True"])
    assert config.lr == 1.0
    assert config.adam

    # "+"
    config = argdcls.load(Config, ["lr=1.0", "+addon=3"])
    assert config.lr == 1.0
    assert not config.adam
    assert config.addon == 3  # type: ignore

    # "++"
    config = argdcls.load(Config, ["++lr=1.0", "++adam=True", "++addon=3"])
    assert config.lr == 1.0
    assert config.adam
    assert config.addon == 3  # type: ignore


def test_parse():
    # "*"
    param_t, key, val = _parse("@lr=1.0")
    assert param_t == "*"
    assert key == "lr"
    assert val == 1.0

    # ""
    param_t, key, val = _parse("lr=1.0")
    assert param_t == ""
    assert key == "lr"
    assert val == 1.0

    # "+"
    param_t, key, val = _parse("+lr=1.0")
    assert param_t == "+"
    assert key == "lr"
    assert val == 1.0

    # "++"
    param_t, key, val = _parse("++lr=1.0")
    assert param_t == "++"
    assert key == "lr"
    assert val == 1.0
