# npt-promote
Mypy plugin to add type promotions between NumPy and builtin data types.

The main use case for this plugin is to enable generic use of `int` and `float`
type annotations with NumPy arrays, e.g.

``` python
import numpy as np
import numpy.typing as npt

x: npt.NDArray[float] = np.array((42.0))
```

## Installation

Dependencies:
- [mypy](https://github.com/python/mypy)
- [NumPy](https://github.com/numpy/numpy)

Install it with:

``` bash
python -m pip install npt-promote
```

Alternatively, add `npt-promote` as a project dependency wherever `mypy` is used,
e.g. as an optional dev requirement in `pyproject.toml`:

``` toml
[project.optional-dependencies]
dev = ["mypy", "npt-promote"]
```

## Usage

To enable the plugin, it must be added to your project's mypy configuration file
along with NumPy's mypy plugin. E.g. add the following to `pyproject.toml`:

``` toml
[tool.mypy]
plugins = [
  'numpy.typing.mypy_plugin',
  'npt_promote',
]
```

## pre-commit
To use the plugin with `mypy` as a `pre-commit` hook, it must be added as a
dependency, e.g. add the following to `.pre-commit-config.yaml`:
``` yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  hooks:
  - id: mypy
    additional_dependencies: [
      "npt-promote"
    ]
```

## Testing

First, install `npt-promote` with:
``` bash
python -m pip install npt-promote[dev]
```

To run the tests, execute:
``` bash
pytest --mypy-only-local-stub
```
