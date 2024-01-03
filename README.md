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

Add `npt-promote` as a project dependency, e.g. as an optional dev requirement
in `pyproject.toml`:

``` toml
[project.optional-dependencies]
dev = ["mypy", "npt-promote"]
```

To use the plugin with `mypy` as a `pre-commit` hook, add the following to `.pre-commit-config.yaml`:
``` yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  hooks:
  - id: mypy
    additional_dependencies: [
      "npt-promote"
    ]
```

To enable the plugin, it must be added to your project's mypy configuration file
along with NumPy's mypy plugin. E.g. add the following to `pyproject.toml`:

``` toml
[tool.mypy]
plugins = [
  'numpy.typing.mypy_plugin',
  'npt_promote',
]
```

To run the tests, execute:
```
pytest --mypy-only-local-stub
```

