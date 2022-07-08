import sys
from dataclasses import _MISSING_TYPE, field, fields, make_dataclass
from typing import Any, List, Optional, Tuple, Type, TypeVar

T = TypeVar("T")


def load(datacls: Type[T], inputs: Optional[List[str]] = None) -> T:
    if inputs is None:
        inputs = sys.argv[1:]
    params = [_parse(s) for s in inputs]

    # Each key is unique
    keys = set([])
    for _, key, _ in params:
        if key in keys:
            raise ValueError(f"There are duplicate parameters: {key}")
        keys.add(key)

    a_fields = [(key, val) for param_t, key, val in params if param_t == "@"]
    n_fields = [(key, val) for param_t, key, val in params if param_t == ""]
    p_fields = [(key, val) for param_t, key, val in params if param_t == "+"]
    pp_fields = [(key, val) for param_t, key, val in params if param_t == "++"]

    field_defaults = {f.name: f.default for f in fields(datacls)}
    field_names = [f.name for f in fields(datacls)]

    # assert "@" params
    for key, val in a_fields:
        if type(field_defaults[key]) != _MISSING_TYPE:
            raise ValueError(
                f'Parameter "{key}" must have no default value but have default value: "{field_defaults[key]}". You may use "{key}={val}" instead.'
            )
        if key not in field_defaults:
            raise ValueError(
                f'Parameter "{key}" not in {field_names}. You may use "+{key}={val}" instead.'
            )

    # assert "" params
    for key, val in n_fields:
        if key not in field_names:
            raise ValueError(
                f'Parameter "{key}" not in {field_names}. You may use "+{key}={val}" instead.'
            )

    # assert "+" fields
    for key, val in p_fields:
        if key in field_names:
            raise ValueError(
                f'Parameter "{key}" in {field_names}. You may use "{key}={val}" instead.'
            )

    # set required params
    require_fields = []
    for key, val in a_fields + n_fields + pp_fields:
        if key in field_names and type(field_defaults[key]) == _MISSING_TYPE:
            require_fields.append((key, val))

    x: T = datacls(**dict(require_fields))  # type: ignore

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
    if "=" not in s:
        raise ValueError(f"You may have forgot to use = for specifying parametsrs: {s}")
    if len(s.split("=")) != 2:
        raise ValueError(f"Wrong parameter inputs: {s}")
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

    if param_t not in ["", "@", "+", "++"]:
        raise ValueError("Wrong parameter type is specified: f{param_t}")
    if "=" in key:
        raise ValueError("Wrong parameter key: f{key}")
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
