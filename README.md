[![ci](https://github.com/sotetsuk/argdcls/actions/workflows/ci.yml/badge.svg)](https://github.com/sotetsuk/argdcls/actions/workflows/ci.yml)
[![python-version](https://img.shields.io/pypi/pyversions/argdcls)](https://pypi.org/project/argdcls)
[![pypi](https://img.shields.io/pypi/v/argdcls)](https://pypi.org/project/argdcls)

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
print(config)
```

```sh
$ python3 main.py @lr=1.0
Config(lr=1.0, adam=False)
$ python3 main.py lr=1.0 adam=True
Config(lr=1.0, adam=True)
```

`@param=value` avoids overwriting the default values.

## License
MIT
