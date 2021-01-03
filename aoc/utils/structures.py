from __future__ import nested_scopes
from typing import List, Any, Dict, Hashable, Generic, TypeVar, Optional, Tuple


K = TypeVar('K', bound=Hashable)


class Tree(Generic[K]):
    """
    Tree with arbitrary # of children
    """
    parent: Optional['Tree']
    children: Dict[K, 'Tree']
    node_id: K
    attr: Dict[str, Any]
    _nodes: Dict[K, 'Tree']     # cache of all direct & indirect children, may have old data upon node parent change.

    @staticmethod
    def of_edges(edges: List[Tuple[K, K]]):
        root = Tree('root')
        for parent, child in edges:
            if parent in root:
                if child in root:
                    root.add_child(parent, root[child])
                else:
                    root.new_child(parent, child)
            else:
                if child in root:
                    parent_node = Tree(parent)
                    root.insert_parent(child, parent_node)
                else:
                    root.new_child('root', parent)
                    root.new_child(parent, child)
        return root

    def __init__(self, node_id: K, /, **attrs):
        self.children = {}
        self.parent = None
        self.node_id = node_id
        self.attr = dict(attrs)
        self._nodes = {node_id: self}

    def add_child(self, parent_id: K, node: 'Tree'):
        """
        Before: ? -> node -> [...]; parent
        After: ? -> [...]; parent -> node -> [...]
        """
        original_parent = node.parent
        if original_parent is not None:
            del original_parent.children[node.node_id]

        parent_pointer = self._nodes[parent_id]
        node.parent = parent_pointer
        parent_pointer.children[node.node_id] = node

        while parent_pointer is not None:
            parent_pointer._nodes.update(node._nodes)
            parent_pointer = parent_pointer.parent
        return self

    def new_child(self, parent_id: K, node_id: Optional[K] = None, /, **attrs):
        """
        Before: parent -> [...]
        After: parent -> [Tree(node_id), ...]
        """
        node_id = node_id if node_id is not None else "{nid}_child{x}".format(nid=self.node_id, x=len(self.children))
        child = Tree(node_id, **attrs)
        self.add_child(parent_id, child)
        return child

    def insert_parent(self, target_id: K, node: 'Tree'):
        """
        Before: parent -> [target -> [...], ...]; node
        After: parent -> [node -> target -> [...], ...]
        """
        target = self._nodes[target_id]
        original_parent = target.parent
        node.add_child(node.node_id, target)

        return self.add_child(original_parent.node_id, node)

    def remove_node(self, target_id: K):
        target = self._nodes[target_id]
        parent = target.parent
        if parent is None:
            raise ValueError("Nothing to do to remove root node.")

        for child in target.children.values():
            parent.add_child(parent.node_id, child)

        del parent.children[target_id]

        while parent is not None:
            del parent._nodes[target_id]
            parent = parent.parent

    def refresh_cache(self):
        new_nodes_cache = {self.node_id: self}
        for child in self.children.values():
            child.refresh_cache()
            new_nodes_cache.update(child._nodes)
        self._nodes = new_nodes_cache

    def print_tree(self, indent: int = 0):
        print(f"{' ' * indent}{self.node_id}({self.attr})")
        for child in self.children.values():
            child.print_tree(indent + 1)

    def __contains__(self, key: K):
        return key in self._nodes

    def __getitem__(self, key) -> 'Tree':
        return self._nodes[key]

    def __str__(self):
        return f"Node<{self.node_id}>(p<{self.parent}>, c~{len(self.children)}, attr:{self.attr})"

    def __repr__(self):
        return str(self)