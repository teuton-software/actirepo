import time
from pprint import pprint
from actirepo.moodle.quiz import Quiz
from actirepo.activity import Activity
from actirepo.category import Category
from actirepo.repo import Repo

#!/usr/bin/env python3

import os
import argparse
import sys
import traceback
import tabulate

import actirepo.activity as activity
import actirepo.repo as repo

from actirepo.__init__ import __module__, __project_name__, __project_version__, __project_description__
from actirepo.utils.dict_utils import trim_all_keys

def list_activities(directory="."):
    activities = repo.list_activities(directory)
    print(f'Listando actividades en "{directory}"')
    if not activities:
        print("No hay actividades")
        return
    activities = trim_all_keys(activities, ['name', 'description', 'category', 'path', 'total'])
    headers = [ 'Nombre', 'Descripción', 'Categoría', 'Directorio', 'Preguntas' ]
    rows =  [x.values() for x in activities]
    print(tabulate.tabulate(rows, headers, tablefmt='grid', maxcolwidths=50))
    print(f'Total: {len(activities)} actividad(es) encontrada(s)')

def create_activity(directory=".", force = False):
    print(f'Creando el descriptor de la actividad "{activity.ACTIVITY_FILE}" en el directorio "{directory}"...')
    try:
        activity.create_activity(directory, force)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def create_readmes(directory, recursive, force):
    try:
        repo.create_readmes(directory, recursive, force)
    except Exception as e:
        traceback.print_exc(e)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
def create_images(questions_file, html):
    try:
        activity.create_images(questions_file, html)
    except Exception as e:
        traceback.print_exc(e)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def create_repo(directory=".", force = False):
    try:
        repo.create_repo(directory, force)
    except Exception as e:
        traceback.print_exc(e)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():

    # declara un HelpFormatter personalizado para reemplazar el texto 'usage:' por 'Uso:'
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix='Uso: '):
            if usage is not argparse.SUPPRESS:
                args = usage, actions, groups, prefix
                self._add_item(self._format_usage, args)

    # define el parser
    parser = argparse.ArgumentParser(prog=__module__, description='Organizador de cuestionarios Moodle en formato XML.', epilog='¡Espero que te sea útil!', add_help=False, formatter_class=CustomHelpFormatter)

    # define los comandos (mutuamente excluyentes)
    commands = parser.add_argument_group('Comandos')
    commands = commands.add_mutually_exclusive_group(required=True)
    commands.add_argument('-h', '--help', action='store_true', help='Muestra esta ayuda y termina')
    commands.add_argument('-v', '--version', action='version', help='Mostrar versión', version=f'%(prog)s {__project_version__}')
    commands.add_argument('-A', '--activity', metavar='RUTA', nargs='?', const='.', help='Crea el README de la actividad en el directorio especificado (o directorio actual si no se proporciona)')
    commands.add_argument('-C', '--category', metavar='RUTA', nargs='?', const='.', help='Crea el README de la categoría en el directorio especificado (o directorio actual si no se proporciona)')
    commands.add_argument('-R', '--repository', metavar='RUTA', nargs='?', const='.', help='Crea el README del repositorio en el directorio especificado (o directorio actual si no se proporciona)')

    # define las opciones adicionales a los comandos
    options = parser.add_argument_group('Opciones')
    options.add_argument('--create', action='store_true', help='Crea los metadatos del artefacto especificado (actitidad, categoría o repositorio)')
    options.add_argument('--readme', action='store_true', help='Crea el archivo README.md')
    options.add_argument('-r', '--recursive', action='store_true', help='Se aplica el comando de forma recursiva. Se puede combinar con --readme')
    options.add_argument('-f', '--force', action='store_true', help='Forzar la creación de README.md aunque no sea necesario. Se puede combinar con --readme')

    # parsea los argumentos
    args = parser.parse_args()

    start_time = time.time()

    # lógica según las opciones
    if args.help:
        parser.print_help()
        return

    elif args.activity:
        if args.create:
            Activity.create(args.activity)
        elif args.readme:
            activity = Activity(args.activity)
            activity.create_readme(args.force)

    elif args.category:
        if args.create:
            Category.create(args.category)
        elif args.readme:
            category = Category(args.category)
            category.create_readme(args.recursive)

    elif args.repository:
        if args.create:
            Repo.create(args.repository)
        elif args.readme:
            repo = Repo(args.repository)
            repo.create_readme(args.recursive)

    print(f"Elapsed time: {time.time() - start_time:.2f} s")

if __name__ == "__main__":
    main()

