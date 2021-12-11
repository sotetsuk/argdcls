import sys
from typing import Any, List, Optional, Tuple, Type, TypeVar

T = TypeVar("T")


def load(datacls: Type[T], inputs: Optional[List[str]] = None) -> T:
    if inputs is None:
        inputs = sys.argv[1:]
    args = {}
    for s in inputs:
        param_t, key, val = _parse(s)
        if param_t == "":
            args[key] = val

    return datacls(**args)


def _parse(
    s: str,
) -> Tuple[str, str, Any]:
    s = s.strip().strip("\n")

    # parse param_t
    param_t = ""
    if s.startswith("++"):
        param_t = "++"
        s = s[2:]
    if s.startswith("+"):
        param_t = "+"
        s = s[1:]

    # parse key
    assert "=" in s
    assert len(s.split("=")) == 2
    key, val = s.split("=")

    x: Any = val
    # parse val
    if x == "None":
        x = None
    elif x == "True":
        x = True
    elif x == "False":
        x = False
    elif _is_num(x):
        if _is_integer(x):
            x = int(x)
        else:
            x = float(x)

    assert param_t in ["", "+", "++"]
    assert "=" not in key
    return param_t, key, x


def _is_num(n: str):
    try:
        float(n)
        return True
    except ValueError:
        return False


def _is_integer(n: str):
    assert _is_num(n)
    return float(n).is_integer()
