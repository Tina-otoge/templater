import dataclasses
from dataclasses import dataclass


class Tag:
    pass


@dataclass
class Object:
    DEFAULT_BIND = None
    name: str = None
    bind: dict = None
    position: tuple[int, int] = (0, 0)
    size: tuple[int, int] = (0, 0)
    tags: list[Tag] = dataclasses.field(default_factory=list)

    @classmethod
    def new(cls, type="_unset", **kwargs):
        if type == "_unset":
            if src := kwargs.get("src"):
                if src.endswith(".html") or src.endswith(".html.j2"):
                    type = "html"
                else:
                    type = "image"
        for c in cls.__subclasses__():
            if type == c.__name__.lower():
                return c(**kwargs)
        raise ValueError(f"Unknown object type: {type}")

    def __post_init__(self):
        self.type = self.__class__.__name__.lower()
        if isinstance(self.size, str):
            self.size = tuple(int(i) for i in self.size.split(" "))
        if isinstance(self.position, str):
            self.position = tuple(int(i) for i in self.position.split(" "))
        if isinstance(self.bind, str):
            self.bind = {self.DEFAULT_BIND: self.bind}

    def prepare(self):
        pass

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height


from .html import Html
from .image import Image
from .text import Text
