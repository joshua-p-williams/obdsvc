# obdsvc

# Development / Testing Environment

[ELM327-Emulator](https://github.com/ircama/ELM327-emulator) was used to emulate the ELM327 OBD-II adapter connected to a vehicle.

# Dependencies

* [Click (Command Line Creation Kit)](https://click.palletsprojects.com/)
* [python-OBD](https://python-obd.readthedocs.io/en/latest/)

# References

* [Hypermodern Python](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769)

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

This is a command line app, using the [Click (Command Line Creation Kit)](https://click.palletsprojects.com/).

```bash
# Initially install the dependency
poetry add click

# Can later be updated to the latest minor version
poetry update click

# Update to a newer major version by running
poetry add click^7.0
```

See console app in `console.py`.

Register the app in poetry by adding to the `pyproject.toml`.

```TOML
[tool.poetry.scripts]
obdsvc = "obdsvc.console:main"
```

Install the package in the virtual environment

```bash
poetry install
```

Run the app in teh virtual environment with;

```bash
# Run the app with
poetry run obdsvc

# View usage
poetry run obdsvc --help
```

The OBD support is provided by [python-OBD](https://python-obd.readthedocs.io/en/latest/).

```bash
poetry add obd
```
