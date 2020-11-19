import yaml
from .descriptors import NodeDescriptor, ActionDescriptor
from .game import Game, Node, Action
from .actions import step_into, combine_actions, add_trace, step_out
from .trotter import TrotterState
from time import time


def action_from_entry(entry, node_dict):
    id = entry.get("id")
    return Action(
        apply=combine_actions([
            add_trace,
            step_into([id], node_dict),
        ]),
        descriptor=action_descriptor_from_entry(entry)
    )


def action_descriptor_from_entry(entry):
    return ActionDescriptor(
        title=entry.get("title", "Action"),
    )


def node_from_entry(entry, actions, default):
    return Node(
        descriptor=node_descriptor_from_entry(entry, default),
        actions=actions
    )


def node_descriptor_from_entry(entry, default):
    id = entry.get("id")
    return NodeDescriptor(
        id=id,
        title=entry.get("title", id),
        description=entry.get(
            "description",
            default.get("description", "")
        ),
        background=entry.get(
            "background",
            default.get("background", "")
        ),
        title_image=entry.get(
            "title_image",
            default.get("title_image", "")
        ),
        position=entry.get("position", (0, 0)),
    )


def load_nodes_from_entries(location_entries):
    default = next((
            entry
            for entry in iter(location_entries)
            if entry.get("is_default", False)
        ),
        {}
    )
    entry_dict = {
        entry["id"]: entry for entry in location_entries if "id" in entry
    }
    node_dict = {}
    travel_actions_dict = {}
    back_action = Action(
        apply=combine_actions([
            add_trace,
            step_out
        ]),
        descriptor=ActionDescriptor(title="Back")
    )
    for id, entry in entry_dict.items():
        parent_id = entry.get("parent_id", None)
        if parent_id:
            actions = travel_actions_dict.get(parent_id, None)
            travel_actions_dict[parent_id] = (
                actions
                if actions is not None
                else []
            ) + [action_from_entry(entry, node_dict)]

    for id, entry in entry_dict.items():
        actions = travel_actions_dict.get(id, [])
        parent_id = entry_dict[id].get("parent_id", None)
        node_dict[id] = node_from_entry(
            entry,
            (
                actions
                if parent_id is None
                else (actions + [back_action])
            ),
            default
        )

    return node_dict.values()


def load_nodes(paths):
    entries = []
    for path in paths:
        data = load_yaml(path)
        entries += data.get("locations", [])
    return load_nodes_from_entries(entries)


def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def load_from_data():
    loaded_nodes = load_nodes([
        "data/defaults.yaml",
        "data/uppsala.yaml"
    ])
    trotter = TrotterState(
        player={},
        time=time(),
        trace=[]
    )
    uppsala = next(
        node
        for node in loaded_nodes
        if node.descriptor.id == "uppsala"
    )
    game = Game(
        state=trotter,
        stack=[[uppsala]]
    )
    return game
