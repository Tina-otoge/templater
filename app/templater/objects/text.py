import typing as t
from dataclasses import dataclass

import wand.drawing
import wand.image

from . import Object


@dataclass
class Text(Object):
    DEFAULT_BIND = "text"
    text: str = None
    color: str = "black"
    font_size: int = 12
    font: str = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def convert(self):
        from app.templater.template import debug

        self.img = wand.image.Image(height=1000, width=1000)
        with wand.drawing.Drawing() as draw:
            draw.font = self.font
            draw.gravity = "north_west"
            draw.font_size = self.font_size
            draw.fill_color = self.color
            draw.text(self.x, self.y, self.text)
            draw(self.img)
        self.img.trim()
