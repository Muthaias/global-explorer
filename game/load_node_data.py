import yaml
from .descriptors import NodeDescriptor


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
    node_dict = {
        id: NodeDescriptor(
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
        ) for id, entry in entry_dict.items()
    }
    for id, location in node_dict.items():
        entry = entry_dict[id]
        parent_id = entry.get("parent_id", None)
        if parent_id:
            location.parent = node_dict[parent_id]
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
