# CI/CD implementálása Python projekten

## Előfeltételek

Szoftverek:

* [Parancssoros Git kliens](https://git-scm.com/downloads)
* [Python interpreter](https://www.python.org/downloads/)
* [Visual Studio Code](https://code.visualstudio.com/), extensionök:
  * Python
  * Markdown Execute
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Bármilyen adatbáziskezelő kliens, pl. DBeaver

Regisztráció:

* [GitHub](https://github.com/)

## Python ellenőrzése

```sh
python --version
```

## Virtuális környezet

```sh
python -m venv venv --prompt employees
venv\Scripts\activate
```

## Packaging

[Python Packaging User Guide](https://packaging.python.org/en/latest/)

> A collection of tutorials and references to help you distribute and install Python packages with modern tools.

> The authoritative resource on how to package, publish, and install Python projects using current tools. 

Karbantartja: [Python Packaging Authority](https://www.pypa.io/en/latest/) munkacsoport

[Python Enhancement Proposals (PEP)](https://peps.python.org/)

Python nyelv hivatalos fejlesztési javaslatainak rendszere, egyfajta útmutatóként és döntéshozatali eszközként szolgálnak a Python jövőbeni fejlődési irányait illetően.

* Python script: önmagában futtatható megfelelő Python interpreterrel, ha csak standard library-re van függősége
* Python module: Python file
* Import package: könyvtár, mely Python fájlokat tartalmazhat
* Source Distribution, _sdist_, tömörített fájl (pl. `tar.gz`), mely több könyvtárat és fájlt tartalmazhat (import package és module), önmagában nem használható, build kell hozzá
* Build Distribution, önmagában is használható, egyszerűen oda kell másolni. 
* Wheel egy standard bináris Build Distribution. Hatékonyabb, mint a Source Distribution Package
* Best practice mindkét Distribution előállítása és publikálása

## Packaging flow

* _Source tree_, verziókezelőben tárolt
* Konfigurációst fájl, pl. `pyproject.toml`
* Build egy build toollal, előáll a Source és Build Distribution
* Publikálás, pl. a [Python Package Index-re (PyPI)](https://pypi.org/)

Elkészült és publikált csomag:

* Letölthető
* Saját környezetbe telepíthető (itt történhet build is - konfigurációs fájl alapján)
  * Tipikusan a Python környezet `site-packages` könyvtárába

## Konfigurációs fájl

```toml
[build-system]
requires = ["setuptools>=75.0.0", "wheel"]
build-backend = "setuptools.build_meta"
```

(A `[ ]` karakterekkel jelölt szavak jelzik a TOML fájlban a table-öket.)

Elválik a build frontend és a build backend, köztük egy vékony API. A build backend végzi a konkrét műveleteket, ezek lehetnek a flit, hatch, pdm, poetry, Setuptools, trampolim, és whey.

Build frontend pl. a build, mely egy [PEP 517 ](https://peps.python.org/pep-0517/) build frontend.

A pip a legelterjedtebb eszköz csomagok telepítésére. Amikor telepítés közben buildelni is kell, akkor build frontendként viselkedik.

## Függőségek

PIP frissítése

```sh
python -m pip install --upgrade pip
```

Telepítendő: Visual Studio TOML extension

```toml
[build-system]
requires = ["setuptools>=75.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "employees"
version = "1.0.0"
dependencies = [
    "Flask",
    "psycopg[binary,pool]",
    "Flask-WTF"
]

[project.optional-dependencies]
dev = [
    "build"
]
```

Különválasztva a futtatáshoz és a fejlesztéshez szükséges csomagok.

Csomagok telepítése:

```sh
python -m pip install --editable ".[dev]"
```

[Development mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html): `-e` / `--editable`

Load the code under development directly from the project folder. Az editable package Pythonban egy olyan csomag, amelyet fejlesztési környezetben közvetlenül a forráskódból lehet használni telepítés nélkül.

## Freeze

```sh
python -m pip freeze --exclude-editable > constraints.txt
```

Ha más akarja pont ugyanazt telepíteni:

```shell
python -m pip install -c constraints.txt .
```

## Build

Source distribution előállítása:

```sh
python -m build --sdist .
```

Eredmény a `dist/employees-1.0.0.tar.gz` fájl.

Wheel Build distribution előállítása:

```sh
python -m build --wheel .
```

Eredmény a `dist/employees-1.0.0-py3-none-any.whl` fájl.

## Futtatás

Adatbázis indítása Docker konténerben:

```sh
docker run -d -e POSTGRES_DB=employees -e POSTGRES_USER=employees  -e POSTGRES_PASSWORD=employees  -p 5432:5432  --name employees-postgres postgres
```

```sh
flask --app employees run --debug  
```

## Tesztelés

### Unit tesztek

pytest

```sh
python -m pytest -v test/unit/
```

`-v` verbosity

Tesztek futtathatók Visual Studio Code-ból

Visual Studio Code: Testing / Configure Python Tests

### Integrációs tesztek

```sh
python -m pytest -v test/integration/
```

### E2E tesztek

API:

requests

```sh
python -m pytest -v test/e2e/test_employees_api.py
```

E2E:

Selenium

```sh
python -m pytest -v test/e2e/test_employees_ui.py
```

## Statikus kódellenőrzés



## Dokumentáció

MkDocs

VSCode Extension: PlantUML

Alt + D

## GitHub push

```sh
gh repo create employees-python-2024-11-12 --public --source=. --remote=origin --push
```

## GitHub CLI

Windows PowerShell - adminisztrátor

```sh
choco install gh
```

```sh
gh auth login
```

## GitHub Actions

Javasolt Visual Studio Code extension: GitHub Actions

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