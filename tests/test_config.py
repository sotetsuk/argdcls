from dataclasses import dataclass

import argdcls
from argdcls.config import _parse


@dataclass
class Config:
    lr: float


def test_load_params():
    # no +/++
    config = argdcls.load(Config, ["lr=0.1"])
    assert config.lr == 0.1


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
