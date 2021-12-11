from dataclasses import dataclass

import argdcls
from argdcls.config import _parse


@dataclass
class Config:
    lr: float
    adam: bool = False


def test_load_params():
    # no +/++
    config = argdcls.load(Config, ["lr=0.1"])
    assert config.lr == 0.1

    # ++
    config = argdcls.load(Config, ["lr=0.1", "+adam=True"])
    assert config.adam

    # ++
    config = argdcls.load(Config, ["lr=0.1", "++addon=3"])
    assert config.addon == 3  # type: ignore


def test_parse():
    # no +/++
    param_t, key, val = _parse("lr=0.1")
    assert param_t == ""
    assert key == "lr"
    assert val == 0.1

    # +
    param_t, key, val = _parse("+lr=0.1")
    assert param_t == "+"
    assert key == "lr"
    assert val == 0.1

    # ++
    param_t, key, val = _parse("++lr=0.1")
    assert param_t == "++"
    assert key == "lr"
    assert val == 0.1
