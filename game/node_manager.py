from .load_node_data import (
    load_nodes_from_entries,
    select_by_tags,
    load_entires
)


class NodeManager:
    def __init__(self, dict):
        self.__dict = dict
        self.__node_dict = {node: id for id, node in dict}

    @property
    def entry_points(self):
        for id, node in self.__dict:
            if node.descriptor.is_entry_point:
                yield node

    @property
    def nodes(self):
        return self.__dict.values()

    def node_by_id(self, id):
        return self.__dict[id]

    def id_by_node(self, node):
        return self.__node_dict[node]

    def nodes_by_tags(self, tags, ex_tags=[], count=0):
        return select_by_tags(
            dict=self.__dict,
            tags=tags,
            ex_tags=ex_tags,
            count=count,
        )

    @staticmethod
    def from_data(entries):
        loaded_nodes = load_nodes_from_entries(
            entries
        )
        return NodeManager(loaded_nodes)

    @staticmethod
    def from_paths(paths):
        entries = load_entires(paths)
        return NodeManager.from_data(entries)
