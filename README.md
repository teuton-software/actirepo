# actirepo

Aplicación Python que organiza un repositorio con ficheros de preguntas de Moodle en formato XML.

## ¿Qué hace?

La función principal de `actirepo` es buscar recursivamente en un repositorio actividades y categorías, y generar un fichero `README.md` en cada caso con información relevante sobre la actividad:

- Descripción.

- Dificultad.

- Tipo y cantidad de preguntas.

Esto facilita a cualquier persona a explorar el repositorio de forma sencilla, para encontrar justo el fichero de preguntas Moodle XML que necesita para su aula virtual.

Los distintos tipos de artefactos que contempla `actirepo` son los siguientes:

- **Actividad**: Es todo aquel directorio que contiene un fichero `activity.json` o uno o más ficheros de preguntas en formato Moodle XML. 

- **Categoría**: Es todo aquel directorio que el fichero  descriptor `category.json` o su contenido son sólo subdirectorios. Estos subdirectorios pueden ser a su vez actividades o categorías.

- **Repositorio**: El repositorio es el directorio raíz, que puede tener un fichero descriptor `repo.json`. Es similar a una categoría.

> Los descriptores en formato `.json` contiene metadatos acerca del artefacto, como el nombre, una descripción, autor, dificultad, tags, ...

A continuación se puede observar la estructura de un repositorio de ejemplo:

```
mi-repo
│   repo.json
│
└───category
    │   category.json
    │
    ├───sample1
    │   │   activity.json
    │   │   questions1.xml
    │   └───questions2.xml
    │
    ├───sample2
    │   └───questions.xml
    │
    └───subcategory
            category.json
```

> Los descriptores no son obligatorios. `actirepo` analizará el contenido de cada directorio para saber de qué tipo de artefacto se trata.

Para generar los ficheros `README.md` de cada artefacto, debemos ejecutar el siguiente comando:

```bash
$ actirepo --repository mi-repo --readme --recursive
```

> `actirepo` no sólo generará los ficheros `README.md` de cada artefacto, sino que también generará imágenes con vistas previas de las preguntas de los ficheros de preguntas Moodle XML.

El resultado del comando anterior sería el siguiente:

```
mi-repo
│   README.md
│   repo.json
│
└───category
    │   category.json
    │   README.md
    │
    ├───sample1
    │   │   activity.json
    │   │   questions1.xml
    │   │   questions2.xml
    │   │   README.md
    │   │
    │   └───images
    │       ├───questions1
    │       │       arrastrar-y-soltar-marcadores_1.png
    │       │       arrastrar-y-soltar-sobre-una-imagen_1.png
    │       │       ensayo-adjunto-y-texto_1.png
    │       │       ensayo-fichero-adjunto_1.png
    │       │       ensayo-texto_1.png
    │       │       opcion-multiple-respuesta-multiple_1.png
    │       │       opcion-multiple-respuesta-simple_1.png
    │       │       respuesta-corta_1.png
    │       │       verdaderofalso-con-imagen-adjunta_1.png
    │       │       verdaderofalso-con-imagen-embebida_1.png
    │       │       verdaderofalso_1.png
    │       │
    │       └───questions2
    │               arrastrar-y-soltar-marcadores_1.png
    │               arrastrar-y-soltar-sobre-una-imagen_1.png
    │               ensayo-adjunto-y-texto_1.png
    │               ensayo-fichero-adjunto_1.png
    │               ensayo-texto_1.png
    │               opcion-multiple-respuesta-multiple_1.png
    │               opcion-multiple-respuesta-simple_1.png
    │               respuesta-corta_1.png
    │               verdaderofalso-con-imagen-adjunta_1.png
    │               verdaderofalso-con-imagen-embebida_1.png
    │               verdaderofalso_1.png
    │
    ├───sample2
    │   │   questions.xml
    │   │   README.md
    │   │
    │   └───images
    │       └───questions
    │               arrastrar-y-soltar-marcadores_1.png
    │               arrastrar-y-soltar-sobre-una-imagen_1.png
    │               ensayo-adjunto-y-texto_1.png
    │               ensayo-fichero-adjunto_1.png
    │               ensayo-texto_1.png
    │               opcion-multiple-respuesta-multiple_1.png
    │               opcion-multiple-respuesta-simple_1.png
    │               respuesta-corta_1.png
    │               verdaderofalso-con-imagen-adjunta_1.png
    │               verdaderofalso-con-imagen-embebida_1.png
    │               verdaderofalso_1.png
    │
    └───subcategory
            category.json
            README.md
```

> Actualmente `actirepo` sólo soporta los siguientes tipos de preguntas:
> 
> - Respuesta corta (shortanswer)
> - Selección múltiple (multichoice)
> - Verdadero/Falso (truefalse)
> - Arrastrar y soltar imagen o texto (ddimageortext)
> - Arrastrar y soltar marcador (ddmarker)
> - Ensayo (essay)

## ¿Cómo lo uso?

### Instalar `actirepo` desde GitHub

```bash
pip install git+https://github.com/teuton-software/actirepo.git#egg=actirepo
```

### Mostrar la ayuda

```bash
$ actirepo --help
Uso: actirepo (-h | -v | -A [RUTA] | -C [RUTA] | -R [RUTA]) [--create] [--readme] [-r] [-f]

Organizador de cuestionarios Moodle en formato XML.

Comandos:
  -h, --help            Muestra esta ayuda y termina
  -v, --version         Mostrar versión
  -A [RUTA], --activity [RUTA]
                        Crea el README de la actividad en el directorio especificado (o directorio
                        actual si no se proporciona)
  -C [RUTA], --category [RUTA]
                        Crea el README de la categoría en el directorio especificado (o directorio
                        actual si no se proporciona)
  -R [RUTA], --repository [RUTA]
                        Crea el README del repositorio en el directorio especificado (o directorio
                        actual si no se proporciona)

Opciones:
  --create              Crea los metadatos del artefacto especificado (actitidad, categoría o
                        repositorio)
  --readme              Crea el archivo README.md
  -r, --recursive       Se aplica el comando de forma recursiva. Se puede combinar con --readme
  -f, --force           Forzar la creación de README.md aunque no sea necesario. Se puede combinar
                        con --readme

¡Espero que te sea útil!
```

### Creación de descriptores

Los siguientes comandos permiten crear de forma sencilla e interactiva los descriptores para los distintos tipos de artefactos.

> Si el descriptor ya existe, lo que hará el comando será modificarlo, ofreciendo los valores actuales como valores por defecto.

#### Crear el descriptor de un repositorio

Ejecuta el siguiente comando para generar el descriptor de un repositorio (`repo.json`):

```bash
$ actirepo --repository mi-repo --create
```

Ejemplo de `repo.json`:

```json
{
    "name": "Repositorio de prueba",
    "description": "Este repositorio es para probar actirepo."
}
```

#### Crear el descriptor de una categoría

Ejecuta el siguiente comando para generar el descriptor de una categoría (`category.json`):

```bash
$ actirepo --category mi-repo/category --create
```

Ejemplo de `category.json`:

```json
{
    "name": "Categoría 1",
    "description": "esta es la descripción de la primera categoría.",
    "category": [
        "Mi-repo"
    ],
    "tags": [
        "redes",
        "cables"
    ]
}
```

#### Crear el descriptor de una actividad

Ejecuta el siguiente comando para generar el descriptor de una actividad (`activity.json`):

```bash
$ actirepo --activity mi-repo/category/sample1 --create
```

Ejemplo de `activity.json`:

```json
{
    "name": "Sample1",
    "description": "Test para probar el funcionamiento del organizador de actividades incluyendo activity.json",
    "category": [
        "Mi-repo",
        "Category1"
    ],
    "difficulty": "hard",
    "tags": [
        "test",
        "sample",
        "actirepo",
        "first"
    ],
    "author": {
        "name": "John Doe",
        "email": "jdoe@nasa.com"
    },
    "limit": "5"
}
```

### Generar los ficheros README

Ejecuta el siguiente comando para generar el fichero `README.md` de todos los artefactos de un repositorio:

```bash
$ actirepo --repository mi-repo --readme --recursive
```

Si se especifica la opción `--recursive`, la búsqueda de artefactos será recursiva a partir de la ruta indicada, por lo que si se indica el directorio raíz del repo, se generarán los ficheros README de todas las actividades. 

Si el fichero README existe y es anterior a los cambios realizados en la actividad (metadatos o ficheros de preguntas XML), se volverán a generar el README  y las imágenes. En caso contrario, no se harán cambios.

## Información para desarrolladores

Clonar el repositorio y entrar en el directorio:

```bash
git clone https://github.com/teuton-software/actirepo
cd actirepo
```

Crear un entorno virtual (si no lo hemos hecho antes):

```bash
python -m venv venv
```

Activar el entorno virtual:

```bash
venv\Scripts\activate
```

Instalar el paquete en modo de edición, de modo que se crearán los scripts del paquete y se instalarán las dependencias en el entorno virtual:

```bash
pip install -e .
```

¡Y a programar!

```bash
code .
```

#### Plantillas

Las plantillas utilizadas para generar los ficheros README se encuentran en `src/actirepo/templates`.

Las plantillas utilizadas para generar el código HTML de las preguntas, para luego renderizarlas en PNG, se encuentran en el directorio `src/actirepo/moodle/templates`.

#### Vista previa de las preguntas en HTML

El código HTML de la vista previa de las preguntas, utilizado para crear las plantillas, se extrajo de Moodle utilizando [PageRip](https://chromewebstore.google.com/detail/pagerip-html-+-css-extrac/bkahkocegdkgicmmfpkoeipjmjaeohfn), una extensión de Google Chrome que permite extraer fragmentos de páginas HTML incluyendo el CSS en línea.
