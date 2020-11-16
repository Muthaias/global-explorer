from uuid import uuid4


class Menu:
    def __init__(self, entries, background):
        self.entries = entries
        self.background = background
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def content(self):
        return {
            "type": "menu",
            "background": self.background,
            "actions": self.actions(),
            "backAction": {
                "type": "exit"
            } if self.parent else None
        }

    def actions(self):
        return [
            {
                "type": "navigate",
                "title": entry.title,
                "id": entry.id
            }
            for entry in self.entries
        ]

    def action(self, action):
        if action["type"] == "navigate":
            entry = next(
                (
                    e for e in self.entries
                    if e.id == action["id"]
                ),
                None
            )
            if entry:
                actuator = entry.actuator
                actuator.set_parent(self)
                return actuator
        elif action["type"] == "exit" and self.parent is not None:
            return self.parent


class MenuEntry:
    def __init__(self, type, actuator, title, id=None):
        self.type = type
        self.id = id if id is not None else str(uuid4())
        self.title = title
        self.actuator = actuator
