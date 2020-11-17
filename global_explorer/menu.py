from uuid import uuid4


class Menu:
    def __init__(self, entries, background, allow_back=False):
        self.entries = entries
        self.background = background
        self.allow_back = allow_back

    def content(self):
        return {
            "type": "menu",
            "background": self.background,
            "actions": self.actions(),
        }

    def actions(self):
        return [
            {
                "type": "navigate",
                "title": entry.title,
                "id": entry.id
            }
            for entry in self.entries
        ] + (
            [
                {
                    "type": "exit",
                    "title": "Back",
                    "id": "exit_menu"
                }
            ] if self.allow_back else []
        )

    def action(self, context, action):
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
                return actuator
        elif action["type"] == "exit":
            return None
        return self


class MenuEntry:
    def __init__(self, type, actuator, title, id=None):
        self.type = type
        self.id = id if id is not None else str(uuid4())
        self.title = title
        self.actuator = actuator
