from dataclasses import dataclass

import requests
import wand.image

from . import Object


@dataclass(kw_only=True)
class Image(Object):
    src: str

    def prepare(self):
        if "://" in self.src:
            response = requests.get(self.src)
            response.raise_for_status()
            self.data = response.content
        else:
            with open(self.src, "rb") as f:
                self.data = f.read()

    def convert(self):
        self.img = wand.image.Image(blob=self.data)
