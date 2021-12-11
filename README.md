# Argdcls

A simple tool to use dataclass as your config

## Usage

```py
from dataclasses import dataclass

import argdcls


@dataclass
class Config:
    lr: float
    adam: bool = False


config = argdcls.load(Config)
print(config.lr)
print(config.adam)
print(config.outdir)  # type: ignore
```

```sh
$ python3 main.py lr=1.0 +adam=True ++outdir="results"
1.0
True
results
```

## License
MIT