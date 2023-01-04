# fastapi-shell

[![PyPI - Version](https://img.shields.io/pypi/v/fastapi-shell.svg)](https://pypi.org/project/fastapi-shell)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-shell.svg)](https://pypi.org/project/fastapi-shell)

An ipython shell for fastapi which automatically imports code and optionally
opens a database connection

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install fastapi-shell
```

## Usage

Begin a fastapi-shell session with default import rules:

```console
python -m fastapi_shell
```

Exclude `sandbox` and `tests` modules from session imports:

```console
python -m fastapi_shell --exclude sandbox tests
```

Only include `app` modules in session imports:

```console
python -m fastapi_shell --include app
```

Include `app` modules except for `tests` in session imports:

```console
python -m fastapi_shell --include app --exclude tests
```

Run code during session initialization:

```console
python -m fastapi_shell --run-code "import db; db.connect()"
```

## License

`fastapi-shell` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
