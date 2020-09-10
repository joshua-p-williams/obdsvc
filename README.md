# obdsvc

# Building From Scratch

Python versioning is done via [pyenv](https://github.com/pyenv/pyenv).

```bash
curl https://pyenv.run | bash
```

Python build dependencies added with

```bash
sudo apt update && sudo apt install -y make build-essential \
libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev \
libffi-dev liblzma-dev python-openssl git
```

Version 3.8.5 was initially used

```bash
# Installed on the system
pyenv install 3.8.5

# Local project set to use 3.8.5
pyenv local 3.8.5
```

[Poetry](https://python-poetry.org/) is used for the packaging and dependency management.

```bash
# Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Initialize the project with
poetry init --no-interaction
```

Modify the `pyproject.toml` file to supply additional metadata. (See [TOML](https://github.com/toml-lang/toml) for details on the syntax.)

To ensure test target the correct code we implement a [src layout](https://hynek.me/articles/testing-packaging/).

Poetry will manage our [virtual environment](https://docs.python.org/3/tutorial/venv.html).

```bash
# Install the virual environment
poetry install

# Test the environment
poetry run python
```
