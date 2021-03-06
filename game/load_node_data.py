import yaml
import random
from collections import ChainMap
from .descriptors import NodeDescriptor, ActionDescriptor
from .game import Node, Action
from .actions import (
    step_into,
    combine_actions,
    add_trace,
    step_out,
    step,
    pass_time,
    charge_card,
    select_by_tags,
    add_skill,
    transfer,
    require_skill,
    require_time,
    require_funds,
    require_some,
    require_all,
)


def travel_action_from_entry(entry, node_dict):
    id = entry.get("id")
    opening_hours = entry.get("opening_hours", None)
    return Action(
        apply=combine_actions(
            add_trace,
            step_into([id], node_dict),
        ),
        match=require_time(*opening_hours) if opening_hours else None,
        descriptor=action_descriptor_from_entry(entry, "location")
    )


def action_from_entry(entry, extra_funcs):
    action = entry.get("action", None)
    match = entry.get("match", None)
    return Action(
        apply=(
            parse_apply_func(action, extra_funcs)
            if action
            else None
        ),
        match=(
            parse_apply_func(match, extra_funcs)
            if match
            else None
        ),
        descriptor=action_descriptor_from_entry(entry, "action"),
    )


def parse_apply_func(struct, extra_funcs):
    if not isinstance(struct, list):
        return struct
    funcs = ChainMap(
        {
            "sequence": combine_actions,
            "add_trace": lambda: add_trace,
            "step_out": lambda: step_out,
            "step": lambda: step,
            "pass_time": pass_time,
            "pass_hours": lambda hours: pass_time(hours * 3600),
            "charge_card": charge_card,
            "skill": add_skill,
            "require_skill": require_skill,
            "require_time": require_time,
            "require_funds": require_funds,
            "all": require_all,
            "some": require_some,
            "list": lambda *items: [
                item
                for subitems in items
                for item in (
                    subitems
                    if isinstance(subitems, list)
                    else [subitems]
                )
            ],
            "rlist": lambda items, count: random.sample(items, k=count)
        },
        extra_funcs
    )
    [id, *args] = struct
    if id == "lambda":
        return lambda: parse_apply_func(args[0], extra_funcs)
    else:
        parsed_args = [
            parse_apply_func(s, extra_funcs)
            for s in args
        ]
        func = funcs.get(id)
        result = func(*parsed_args)
        return result


def action_descriptor_from_entry(entry, type):
    return ActionDescriptor(
        title=entry.get("title", "Action"),
        type=type
    )


def node_from_entry(entry, actions, default):
    return Node(
        descriptor=node_descriptor_from_entry(entry, default),
        actions=actions
    )


def node_descriptor_from_entry(entry, default):
    id = entry.get("id")
    e = ChainMap(entry, default)
    return NodeDescriptor(
        id=id,
        title=e.get("title", id),
        description=e.get("description", ""),
        background=e.get("background", ""),
        title_image=e.get("title_image", ""),
        position=e.get("position", (0, 0)),
        type=e.get("actuator", "hub"),
        is_entry_point=e.get("is_entry_point", False),
        tags={tag for tag in e.get("tags", [])}
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
        apply=combine_actions(
            add_trace,
            step_out
        ),
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
            ) + [travel_action_from_entry(entry, node_dict)]

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
    for id, node in node_dict.items():
        entry = entry_dict[id]
        node.set_actions([
            action_from_entry(action_entry, {
                "step_into": lambda ids: step_into(ids, node_dict),
                "transfer": lambda ids: transfer(ids, node_dict),
                "by_tags": (
                    lambda tags, count=0, ex_tags=[]:
                        select_by_tags(tags, node_dict, count, ex_tags)
                ),
            })
            for action_entry in entry.get("actions", [])
        ] + node.actions)

    return node_dict


def load_entires(paths):
    entries = []
    for path in paths:
        data = load_yaml(path)
        entries += data.get("entries", [])
    return entries


def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)
