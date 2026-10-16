# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es

`actirepo` es una CLI en Python (>= 3.12) que recorre un repositorio de ficheros de preguntas Moodle XML y genera un `README.md` por cada actividad, categoría y repositorio, incluyendo imágenes PNG con vistas previas de las preguntas. También se distribuye como GitHub Action compuesta ([action.yml](action.yml)) que instala el paquete desde la rama por defecto de GitHub, ejecuta `actirepo --repository <workspace> --readme --recursive` y hace commit/push de los cambios.

Los textos visibles para el usuario (ayuda de la CLI, plantillas, badges) están en español; mantén ese idioma al tocarlos.

## Comandos

Entorno de desarrollo (Windows, como en el README):

```bash
python -m venv venv
venv\Scripts\activate
pip install -e .          # añade ".[dev]" para black, isort, pytest, bumpver, pip-tools
```

Ejecutar la CLI contra el repositorio de ejemplo de `tests/`:

```bash
actirepo --repository tests --readme --recursive
actirepo --activity tests/category/sample1 --readme --force
actirepo --category tests/category --create      # interactivo, pide los metadatos por consola
```

Regenerar `requirements.txt` tras cambiar dependencias en `pyproject.toml`:

```bash
pip-compile pyproject.toml
```

No hay tests automatizados: `tests/` es un repositorio de ejemplo (fixture) sobre el que se ejecuta la CLI y cuyos `README.md` e `images/` generados están versionados. Para comprobar un cambio, ejecuta la CLI sobre `tests/` y revisa el diff de los README y PNG generados.

La generación de imágenes usa `html2image`, que necesita Google Chrome/Chromium instalado.

## Arquitectura

El punto de entrada es [src/cli/__main__.py](src/cli/__main__.py) (script `actirepo = cli.__main__:main`). Los comandos `-A/-C/-R` son mutuamente excluyentes y se combinan con `--create` (descriptor interactivo) o `--readme`.

Jerarquía de artefactos en [src/actirepo/](src/actirepo/):

- **`Artifact`** ([artifact.py](src/actirepo/artifact.py)): base abstracta; el constructor llama a `load()`, que rellena `self.metadata` con valores por defecto cuando falta el descriptor JSON o alguno de sus campos.
- **`Activity`** ([activity.py](src/actirepo/activity.py)): directorio con `activity.json` o con algún XML cuya raíz sea `<quiz>`. Calcula estadísticas por fichero y genera las imágenes (borra y recrea `images/`) antes de renderizar el README. Solo regenera si el README es más antiguo que el descriptor o los XML, salvo con `force`.
- **`Category`** ([category.py](src/actirepo/category.py)): directorio con `category.json` o que solo contiene subdirectorios. Descubre en `load()` sus actividades y subcategorías (así que construir una categoría parsea todo el subárbol) y agrega sus `Stats`.
- **`Repo`** ([repo.py](src/actirepo/repo.py)): subclase de `Category` que solo cambia `METADATA_FILE` (`repo.json`) y la plantilla.

Los README se renderizan con Jinja2 a partir de [src/actirepo/templates/](src/actirepo/templates/); los filtros (`anchorify`, `difficulty_to_badge`, `quote`, …) se registran en cada `create_readme`, así que un filtro nuevo hay que añadirlo allí.

Capa Moodle en [src/actirepo/moodle/](src/actirepo/moodle/):

- **`Quiz`** ([quiz.py](src/actirepo/moodle/quiz.py)) parsea un XML, agrupa las preguntas por tipo y descarta en silencio los tipos que no estén en `Quiz.SUPPORTED_QUESTIONS`. `generate_images(limit)` renderiza como máximo `limit` preguntas por tipo en `images/<nombre-del-xml>/`.
- **`Question`** ([question.py](src/actirepo/moodle/question.py)) incrusta los adjuntos `@@PLUGINFILE@@` como data URIs, renderiza `moodle/templates/<type>.template.html` y lo convierte a PNG recortado con `utils/image_utils.html2png`. Cada subclase (`MultiChoice`, `TrueFalse`, …) solo extrae los campos que necesita su plantilla.

Para añadir un tipo de pregunta: crear la subclase de `Question`, su plantilla `moodle/templates/<type>.template.html`, registrarla en `Quiz.SUPPORTED_QUESTIONS` y añadir el icono `icons/<type>.svg`. Las plantillas HTML se extrajeron de Moodle con la extensión PageRip (CSS en línea).

## Detalles a tener en cuenta

- La versión está duplicada en [pyproject.toml](pyproject.toml) y en `__project_version__` de [src/actirepo/__init__.py](src/actirepo/__init__.py); hay que cambiar ambas.
- Los README generados enlazan los iconos por URL absoluta (`__icons_url__` en `__init__.py`, que apunta a la rama `master` de `raw.githubusercontent.com`), no a ficheros locales; un icono nuevo no se verá hasta que esté publicado en GitHub.
- `--force` solo se aplica con `--activity`. Con `--category`/`--repository` y `--recursive`, `Category.create_readme` llama a `activity.create_readme(True)`, así que regenera siempre todas las actividades e imágenes.
- `Category.__just_contains_folders` comprueba `os.path.isdir(dirs)` sin unir la ruta del padre, por lo que se evalúa respecto al directorio de trabajo actual.
- Las plantillas y ficheros no Python solo se empaquetan si coinciden con [MANIFEST.in](MANIFEST.in) (`*.md`, `*.toml`, `*.html` bajo `src`).
