import sys
from typing import Any, List, Optional, Tuple


class Config:
    def __init__(self, inputs: Optional[List[str]] = None) -> None:
        if inputs is None:
            inputs = sys.argv[1:]
        self._load_params(inputs)

    def _load_params(self, inputs: List[str]) -> None:
        pass

    @staticmethod
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

        # parse val
        if val == "None":
            val = None
        elif val == "True":
            val = True
        elif val == "False":
            val = False
        elif _is_num(val):
            if _is_integer(val):
                val = int(val)
            else:
                val = float(val)

        assert param_t in ["", "+", "++"]
        assert "=" not in key
        return param_t, key, val


def _is_num(n: str):
    try:
        float(n)
        return True
    except ValueError:
        return False


def _is_integer(n: str):
    assert _is_num(n)
    return float(n).is_integer()
