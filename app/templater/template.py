from dataclasses import dataclass
from pathlib import Path

import wand.image
import yaml

from app.templater.objects import Object


class KeyedList(list):
    KEY = None

    def __getitem__(self, key):
        if isinstance(key, int):
            return super().__getitem__(key)
        if self.KEY is None:
            raise ValueError("KEY not defined")
        for item in self:
            if getattr(item, self.KEY) == key:
                return item
        raise KeyError(key)


class ItemList(KeyedList):
    KEY = "name"


def debug(*obj):
    import datetime
    import json
    import sys

    print(datetime.datetime.now())
    for i, o in enumerate(obj):
        json.dump(o, sys.stdout, indent=2, default=str)
        if i < len(obj) - 1:
            print(" ", end="")
    print()


class Template:
    def __init__(self, path: str):
        path = Path(path)
        if path.is_dir():
            self.dir = path
            path = path / "template.yml"
        else:
            self.dir = False
        with path.open() as f:
            self.data = yaml.safe_load(f)
        self.data.setdefault("settings", {})

    def prepare(self):
        self._process_params()
        self._process_items()
        self._process_bounds()
        for item in self.items:
            item.prepare()

    def convert(self):
        for item in self.items:
            item.convert()
            item.size = item.img.size
        size = self.data["settings"].get("size")
        if size:
            if " " in size:
                size = tuple(int(i) for i in size.split(" "))
            else:
                size = self.items[size].size
        else:
            size = (
                max(i.x2 for i in self.items),
                max(i.y2 for i in self.items),
            )
        width, height = size
        self.image = wand.image.Image(width=width, height=height)
        for item in self.items:
            self.image.composite(item.img, left=item.x, top=item.y)

    def generate(self, output: str = "output.png", **kwargs):
        self.kwargs = kwargs
        self.prepare()
        self.convert()
        self.image.save(filename=str(output))

    ###

    @dataclass
    class ParamDefinition:
        name: str
        required: bool = False
        type: str = "str"

        def get(self, value):
            if self.type == "str":
                if value is None:
                    return ""
                return str(value)
            raise ValueError(
                f"Unsupported type definition {self.type} for param {self.name}"
            )

    def _process_params(self):
        self.params = {}
        for name, data in self.data.get("params", {}).items():
            data = data or {}
            data["name"] = name
            definition = self.ParamDefinition(**data)
            if definition.required and name not in self.kwargs:
                raise ValueError(f"Missing required argument {name}")
            self.params[name] = definition.get(self.kwargs.get(name))

    def _process_items(self):
        self.items = ItemList()

        def process_item(item):
            if isinstance(item, str):
                item = Object.new(src=item)
            else:
                item = Object.new(**item)
            if item.type == "group":
                for item in item.items:
                    process_item(item)
            else:
                self.items.append(item)

        for item in self.data["items"]:
            process_item(item)

    def _process_bounds(self):
        for item in self.items:
            if not item.bind:
                continue
            for property, param in item.bind.items():
                setattr(item, property, self.params[param])
