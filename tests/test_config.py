from dataclasses import dataclass

from argdcls.config import _parse, load


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


@dataclass
class Config:
    lr: float


def test_load_params():
    # no +/++
    config = load(Config, ["lr=0.1"])
    assert config.lr == 0.1
