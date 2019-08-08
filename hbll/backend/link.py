from typing import Any

from attr import dataclass


class Link:
    def get(self):
        raise NotImplementedError


@dataclass
class RecursiveLink(Link):
    node: "Node"
    name: str

    def get(self):
        return getattr(self.node.run(), self.name)


@dataclass(frozen=True)
class StaticLink(Link):
    value: Any

    def get(self):
        return self.value
