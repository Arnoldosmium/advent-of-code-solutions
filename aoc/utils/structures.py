from __future__ import nested_scopes
from typing import List, Any, Dict, Hashable, Generic, TypeVar, Optional


K = TypeVar('K', bound=Hashable)


class Tree(Generic[K]):
    parent: Optional['Tree']
    children: Dict[K, 'Tree']
    node_id: K
    attr: Dict[str, Any]

    def __init__(self, node_id: K, /, **attrs):
        self.children = {}
        self.parent = None
        self.node_id = node_id
        self.attr = dict(attrs)
        self._nodes = {node_id: self}

    def add_child(self, parent_id: K, node: 'Tree'):
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
        node_id = node_id if node_id is not None else "{nid}_child{x}".format(nid=self.node_id, x=len(self.children))
        child = Tree(node_id, **attrs)
        self.add_child(parent_id, child)
        return child

    def insert_parent(self, target_id: K, node: 'Tree'):
        target = self._nodes[target_id]
        original_parent = target.parent
        node.add_child(node.node_id, target)

        return self.add_child(original_parent.node_id, node)

    def __contains__(self, key: K):
        return key in self._nodes

    def __getitem__(self, key) -> 'Tree':
        return self._nodes[key]

    def __str__(self):
        return "Node/{0.node_id}(parent {1}, {2} children, {3})".format(self, self.parent, len(self.children), self.attr)

    def __repr__(self):
        return str(self)