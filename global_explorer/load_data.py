import yaml
from global_explorer import (
    GameLocation,
    LocationVisit,
    LocationHub,
)


def actuator_from_entry(entry):
    actuator_dict = {
        "visit": LocationVisit,
        "hub": LocationHub,
    }
    actuator_id = entry.get("actuator", "hub")
    return actuator_dict.get(actuator_id, LocationHub)()


def locations_from_entries(location_entries):
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
    location_dict = {
        id: GameLocation(
            title=entry.get("title", id),
            id=id,
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
            actions=None if "parent_id" in entry else [],
            actuator=actuator_from_entry(entry)
        ) for id, entry in entry_dict.items()
    }
    for id, location in location_dict.items():
        entry = entry_dict[id]
        parent_id = entry.get("parent_id", None)
        if parent_id:
            location.parent = location_dict[parent_id]
    return location_dict.values()


def load_locations(paths):
    entries = []
    for path in paths:
        data = load_yaml(path)
        entries += data.get("locations", [])
    return locations_from_entries(entries)


def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)
