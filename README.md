
```shell
python --version
```

```shell
python -m venv venv --prompt employees
venv\Scripts\activate
python -m pip install --upgrade pip
```

* `pyproject.toml` configuration file
* [setuptools](https://setuptools.pypa.io/en/latest/)
* [build](https://peps.python.org/pep-0517/) back end

Visual Studio TOML extension

Development mode: `-e` / `--editable`
    load the code under development directly from the project folder
    editable package Pythonban egy olyan csomag, amelyet fejlesztési környezetben közvetlenül a forráskódból lehet használni telepítés nélkül

```shell
python -m pip install --editable .
```

https://setuptools.pypa.io/en/latest/userguide/development_mode.html

```
Building wheels for collected packages: employees
  Building editable for employees (pyproject.toml) ... done
  Created wheel for employees: filename=employees-1.0.0-0.editable-py3-none-any.whl size=1231 sha256=c0d19cc869f7ba138d91dd4538fd91e382b09c28b62c868d20f68c06a1108ec3
  Stored in directory: C:\Users\iviczian\AppData\Local\Temp\pip-ephem-wheel-cache-20bodhht\wheels\aa\1a\c1\8c8803bdc676db5b4038e55afda2c3bf718a30b103976b6389
Successfully built employees
```

psycopg, ami a 3-as verzió, jobb a teljesítménye

DBeaver

```shell
docker run -d -e POSTGRES_DB=employees -e POSTGRES_USER=employees  -e POSTGRES_PASSWORD=employees  -p 5432:5432  --name employees-postgres postgres
```

```sh
python -m pip freeze --exclude-editable > constraints.txt
```

Ha más akarja pont ugyanazt telepíteni:

```shell
python -m pip install -c constraints.txt .
```

```shell
flask --app employees run --debug  
```

pytest

```sh
python -m pip install --editable ".[dev]"
```

Markdown Execute Visual Studio extension

```sh
python -m pytest -v test/unit/
```

`-v` verbosity

Integrációs tesztek

E2E tesztek

## GitHub CLI

Windows PowerShell - adminisztrátor

```sh
choco install gh
```

```sh
gh auth login
```

## Act

```sh
gh extension install https://github.com/nektos/gh-act
```

GitHub Actions Visual Studio Code extension

https://github.com/marketplace

```sh
gh act push
```

Medium