from argparse import ArgumentParser
from pathlib import Path

from app.templater import Template

parser = ArgumentParser()
parser.add_argument("template", type=Path)
parser.add_argument("arguments", nargs="*")
args = parser.parse_args()

arguments = {}
for arg in args.arguments:
    if "=" not in arg:
        raise ValueError(f"Invalid argument {arg}")
    key, value = arg.split("=")
    arguments[key] = value
Template(args.template).generate(**arguments)
