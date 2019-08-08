from itertools import chain
from typing import Any, Dict, NamedTuple, Optional, Set, Type, List
from uuid import UUID

from hbll.backend.link import RecursiveLink, StaticLink, Link
from .manager_schema import Function

from toposort import toposort


# Map inputname -> (output_node, output_name)
class Connection(NamedTuple):
    id: UUID
    name: str


Links = Dict[str, Connection]


class Node:
    def __init__(self, func: Type[Function], id: UUID):
        self.func_type = func
        self.inputLinks: Dict[str, Optional[Link]] = {
            name: StaticLink(None) for name in self.func_type.InputTypes.keys()
        }
        self.func: Optional[Function] = None
        self.id = id

        self.results = None
        self.has_run: bool = False

        self.settings = None

    def next_frame(self):
        self.results = None
        self.has_run = False

    def reset_links(self):
        self.inputLinks: Dict[str, Optional[Link]] = {
            name: StaticLink(None) for name in self.func_type.InputTypes.keys()
        }

    def ensure_init(self):
        if self.func is not None:
            return

        self.func = self.func_type(self.settings)

    def dispose(self):
        if self.func is None:
            return

        self.func.dispose()
        self.func = None

    def set_static_link(self, key: str, item: Any):
        self.inputLinks[key] = StaticLink(item)

    def set_static_links(self, vals: Dict[str, Any]):
        for key, item in vals.items():
            self.set_static_link(key, item)

    def run(self):
        if self.has_run:
            return self.results

        self.ensure_init()

        inputs = {name: link.get() for name, link in self.inputLinks.items()}
        inputs = self.func_type.Inputs(**inputs)

        self.results = self.func.run(inputs)
        self.has_run = True

        return self.results


class Pipeline:
    def __init__(self):
        self.nodes: Dict[UUID, Node] = {}
        self.adjList: Dict[Node, Set[Node]] = {}
        self.run_order: List[Node] = []

    def run(self):
        if not self.run_order:
            self.run_order = list(chain.from_iterable(toposort(self.adjList)))

        for n in self.run_order:  # Each node to be processed
            n.run()

    def create_node(self, func: Type[Function], uuid: UUID):
        """
        The caller is responsible for calling
        pipeline.create_links(node, ...) and node.set_staticlinks(...),
        and setting node.settings as appropriate
        """
        self.run_order.clear()
        temp = Node(func, uuid)

        self.adjList[temp] = set()
        self.nodes[uuid] = temp

        return temp

    def create_links(self, input_node_id, links: Links):
        self.run_order.clear()
        input_node = self.nodes[input_node_id]

        for input_name, conn in links.items():
            output_node = self.nodes[conn.id]
            self.adjList[input_node].add(output_node)

            input_node.inputLinks[input_name] = RecursiveLink(output_node, conn.name)

    def prune_nodetree(self, new_node_ids):
        old_node_ids = set(self.nodes.keys())
        new_node_ids = set(new_node_ids)

        for node in self.nodes.values():
            node.reset_links()

        # remove deleted nodes

        for uuid in old_node_ids - new_node_ids:
            self.nodes[uuid].dispose()
            del self.nodes[uuid]
