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
        return "", "", None
