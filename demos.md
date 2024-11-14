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

## Statikus kódellenőrző eszközök

* Black: kódformázás
* Flake8: PEP8 és clean code
* Mypy: statikus típusellenőrzés
* Pylint: részletes kódminőség ellenőrzés
* isort: importok rendezése
* Bandit: biztonsági hibák és sebezhetőségek

* Ruff
  * 10-100x gyorsabb, mint a Flake8 vagy Black
  * `pyproject.toml` support
  * Drop-in parity with Flake8, isort, and Black

```sh
pre-commit autoupdate --repo https://github.com/pycqa/isort
```

Visual Studio Code: Workspace Settings

```json
"editor.rulers": [79]
```

A black és a flake8 eltérő kódszélességi szabványt alkalmaz.
Alapértelmezetten a black 88 karakteres sormaximumot állít be, míg a flake8 79 karaktert használ.

A flake8 nem támogatja közvetlenül a `pyproject.toml` fájlon keresztüli konfigurálást, de helyette használhatod a .flake8
konfigurációt.

A black támogatja a `pyproject.toml` fájlon keresztüli konfigurálást:

```toml
[tool.black]
line-length = 79
```

error: Library stubs not installed for "requests"  [import-untyped]
note: Hint: "python3 -m pip install types-requests"
note: (or run "mypy --install-types" to install all missing stub packages)
note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports

isort és a black összeakad, mert a hosszú sort másképp formázzák:

https://github.com/psf/black/issues/127

Megoldás:

```toml
[tool.isort]
multi_line_output=3
include_trailing_comma=true
```

```sh
mypy src
```

```sh
pylint src
```

```sh
bandit -c pyproject.toml -r test
```

### Ruff

Markdown dokumentumokban lévő kódokat is tud kezelni

### pre-commit

[pre-commit](https://pre-commit.com/)

> Multi-language package manager for pre-commit hook

```sh
pre-commit run --all-files
```

`.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
    -   id: black

-   repo: https://github.com/PyCQA/flake8
    rev: 7.1.1
    hooks:
    -   id: flake8

-   repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
    -   id: isort
```

`pyproject.toml`

```toml
[project.optional-dependencies]
dev = [
    "black",
    "flake8",
    "isort",
]

[tool.black]
line-length = 79

[tool.isort]
multi_line_output=3
include_trailing_comma=true
```

`.flake8`

```toml
[flake8]
max-line-length = 79
```

#### pylint virtuális environmentben

pylint lokálisan konfigurálandó, különben a hibaüzenet: `Unable to import '...' (import-error)`

Ugyanis külön virtual environmentben dolgozik, és ott nincsenek a függőségek.

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

### Act

```sh
gh extension install https://github.com/nektos/gh-act
```

GitHub Actions Visual Studio Code extension

https://github.com/marketplace

```sh
gh act push
```

Medium

### venv

* Minden step új bash shell-t indít
* Be kell állítani, hogy a `venv/bin` könyvtár mindig benne legyen a path-ban

```yaml
echo ".venv/bin" >> $GITHUB_PATH
```

* Viszont be kell állítani, hogy innentől ezt a könyvtárat kell cache-elni, valamint hogy mely állományok változásakor kell update-elni a cache-t
