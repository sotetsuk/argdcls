from argdcls.config import Config


def test_parse():
    # basic usage
    param_t, key, val = Config._parse("+lr=0.1")
    assert param_t == "override"
    assert key == "lr"
    assert val == 0.1
