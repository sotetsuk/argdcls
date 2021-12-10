from argdcls.config import Config


def test_parse():
    # no +/++
    param_t, key, val = Config._parse("lr=0.1")
    assert param_t == ""
    assert key == "lr"
    assert val == 0.1

    # +
    param_t, key, val = Config._parse("+lr=0.1")
    assert param_t == "+"
    assert key == "lr"
    assert val == 0.1

    # ++
    param_t, key, val = Config._parse("++lr=0.1")
    assert param_t == "++"
    assert key == "lr"
    assert val == 0.1
