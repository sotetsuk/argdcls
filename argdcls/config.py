import sys
from collections import defaultdict
from dataclasses import _MISSING_TYPE, field, fields, make_dataclass
from typing import Any, List, Optional, Tuple


def load(datacls, inputs: Optional[List[str]] = None):
    if inputs is None:
        inputs = sys.argv[1:]
    params = [_parse(s) for s in inputs]

    # Each key is unique
    keys: defaultdict = defaultdict(int)
    for _, key, _ in params:
        keys[key] += 1
    assert all([v == 1 for k, v in keys.items()])

    a_fields = [(key, val) for param_t, key, val in params if param_t == "@"]
    n_fields = [(key, val) for param_t, key, val in params if param_t == ""]
    p_fields = [(key, val) for param_t, key, val in params if param_t == "+"]
    pp_fields = [(key, val) for param_t, key, val in params if param_t == "++"]

    field_defaults = {f.name: f.default for f in fields(datacls)}
    field_names = [f.name for f in fields(datacls)]

    # assert "@" params
    for key, val in a_fields:
        assert (
            type(field_defaults[key]) == _MISSING_TYPE
        ), f'Parameter "{key}" must have no default value but have default value: "{field_defaults[key]}". You may use "{key}={val}" instead.'
        assert (
            key in field_defaults
        ), f'Parameter "{key}" not in {field_names}. You may use "+{key}={val}" instead.'

    # assert "" params
    for key, val in n_fields:
        assert (
            key in field_names
        ), f'Parameter "{key}" not in {field_names}. You may use "+{key}={val}" instead.'

    # assert "+" fields
    for key, val in p_fields:
        assert (
            key not in field_names
        ), f'Parameter "{key}" in {field_names}. You may use "{key}={val}" instead.'

    # set required params
    require_fields = []
    for key, val in a_fields + n_fields + pp_fields:
        if key in field_names and type(field_defaults[key]) == _MISSING_TYPE:
            require_fields.append((key, val))

    x = datacls(**dict(require_fields))

    # set override params
    for key, val in n_fields + pp_fields:
        if key in field_names:
            setattr(x, key, val)

    # set new params
    new_fields = []
    for key, val in p_fields + pp_fields:
        if key not in field_names:
            new_fields.append((key, val))

    x.__class__ = make_dataclass(
        datacls.__name__,
        [(key, type(val), field(default=val)) for key, val in new_fields],
        bases=(datacls,),
    )

    return x


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
    if s.startswith("@"):
        param_t = "@"
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

    assert param_t in ["", "@", "+", "++"]
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
    try:
        int(n)
        return True
    except ValueError:
        return False
