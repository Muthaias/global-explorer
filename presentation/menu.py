class Menu:
    def __init__(self, entries, background, allow_back=False):
        all_entries = entries + ([
            MenuAction(MenuEntry("navigation", "Back"), self)
        ] if allow_back else [])
        self.__actions = [
            MenuAction(entry, self) for entry in all_entries
        ]
        self.__allow_back = allow_back
        self.background = background

    def content(self, context):
        return {
            "type": "menu",
            "background": self.background,
            "actions": [{
                "type": "navigate",
                "id": context.get_id(action),
                "title": action.title,
            } for action in self.actions],
        }

    @property
    def actions(self):
        return self.__actions

    def action(self, context, action, value=None):
        if action.owner is self:
            return action.actuator

        return self


class MenuAction:
    def __init__(self, entry, owner):
        self.__owner = owner
        self.__entry = entry

    @property
    def owner(self):
        return self.__owner

    @property
    def type(self):
        return self.__entry.type

    @property
    def title(self):
        return self.__entry.title

    @property
    def actuator(self):
        return self.__entry.actuator


class MenuEntry:
    def __init__(self, type, title, actuator=None):
        self.type = type
        self.title = title
        self.actuator = actuator
