from uuid import uuid4

class Menu:
    def __init__(self, entries, background, exit_actuator = None):
        self.entries = entries
        self.background = background
        self.exit_actuator = exit_actuator
    
    def content(self):
        return {
            "type": "menu",
            "background": self.background,
            "actions": self.actions(),
            "backAction": {
                "type": "exit"
            } if self.exit_actuator else None
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
            entry = next((e for e in self.entries if e.id == action["id"]), None)
            if entry:
                actuator = entry.actuator
                if hasattr(actuator, "exit_actuator"):
                    actuator.exit_actuator = self
                return actuator
        elif action["type"] == "exit" and self.exit_actuator != None:
            return self.exit_actuator 

class MenuEntry:
    def __init__(self, type, actuator, title, id = None):
        self.type = type
        self.id = id if id != None else str(uuid4())
        self.title = title
        self.actuator = actuator