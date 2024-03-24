#!/usr/bin/env python3

import os
import argparse
import sys
import traceback
import tabulate

import actirepo.activity as activity
import actirepo.repo as repo

from actirepo.__init__ import __version__, __module__
from actirepo.dict_utils import trim_all_keys

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

def create_readmes(directory, force=False):
    try:
        repo.create_readmes(directory, force)
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
    parser = argparse.ArgumentParser(prog=__module__, description='Organizador de actividades', epilog='¡Espero que te sea útil!', add_help=False, formatter_class=CustomHelpFormatter)

    # define los comandos (mutuamente excluyentes)
    commands = parser.add_argument_group('Comandos')
    commands = commands.add_mutually_exclusive_group(required=True)
    commands.add_argument('-h', '--help', action='store_true', help='Muestra esta ayuda y termina')
    commands.add_argument('-v', '--version', action='version', help='Mostrar versión', version=f'%(prog)s {__version__}')
    commands.add_argument('-l', '--list', metavar='RUTA', nargs='?', const='.', help='Listar actividades de forma recursiva en el directorio especificado (o directorio actual si no se proporciona)')
    commands.add_argument('-i', '--images', metavar='FICHERO', help='Genera imágenes de las preguntas de una actividad')
    commands.add_argument('-R', '--readme', metavar='RUTA', help='Crear README.md para repositorio y/o actividad en el directorio especificado. Se puede combinar con "-r".')
    commands.add_argument('-C', '--create-activity', metavar='RUTA', nargs='?', const='.', help='Crear los metadatos de la actividad en el directorio especificado (o directorio actual si no se proporciona)')
    commands.add_argument('-c', '--create-repo', metavar='RUTA', nargs='?', const='.', help='Crear los metadatos del repositorio en el directorio especificado (o directorio actual si no se proporciona)')

    # define las opciones adicionales a los comandos
    options = parser.add_argument_group('Opciones')
    options.add_argument('-r', '--recursive', action='store_true', help='Buscar actividades recursivamente en subdirectorios. Se puede combinar con --readme y --create')
    options.add_argument('-f', '--force', action='store_true', help='Forzar la creación de README.md aunque no sea necesario')
    options.add_argument('-H', '--html', action='store_true', help='Genera también el HTML de las preguntas al generar las imágenes')

    # parsea los argumentos
    args = parser.parse_args()

    # lógica según las opciones
    if args.help:
        parser.print_help()
    elif args.list:
        list_activities(args.list)
    elif args.images:
        create_images(args.images, args.html)
    elif args.readme:
        if args.recursive:
            create_readme_all_activities(args.readme, args.force)
        else:
            cre
        create_readme_all_activities(args.readme, args.recursive, args.force)
    elif args.create_activity:
        create_activity(args.create_activity, args.force)
    elif args.create_repo:
        create_repo(args.create_repo, args.force)

if __name__ == "__main__":
    main()