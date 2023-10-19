from dataclasses import dataclass

from .image import Image


@dataclass(kw_only=True)
class Html(Image):
    src: str
