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
$ python3 main.py lr=1.0 adam=True +outdir=results
Config(lr=1.0, adam=True, outdir='result')
```

|| `@param` | `param` | `+param` | `++param` |
|:---|:---:|:---:|:---:|:---:|
|w/o default value|OK|OK|Error|OK|
|w/ default value|Error|OK|Error|OK|
|not dfined|Error|Error|OK|OK|

## License
MIT
