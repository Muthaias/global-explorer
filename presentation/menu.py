class Menu:
    def __init__(self, entries, background, allow_back=False):
        all_entries = entries + ([
            MenuEntry("navigate", "Back")
        ] if allow_back else [])
        self.__actions = [
            MenuAction(entry, self) if isinstance(entry, MenuEntry) else entry
            for entry in all_entries
        ]
        self.__allow_back = allow_back
        self.background = background
        self.__props = {}

    def content(self, context):
        return {
            "type": "menu",
            "background": self.background,
            "actions": [{
                "type": action.type,
                "id": context.get_id(action),
                "title": action.title,
                "value": action.value,
            } for action in self.actions],
        }

    @property
    def props(self):
        return self.__props

    @property
    def actions(self):
        return self.__actions

    def action(self, context, action, value=None):
        if action.owner is self:
            return action.apply(context, value)

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
    def value(self):
        return self.__entry.value

    def apply(self, context, value):
        if callable(self.__entry.actuator):
            return self.__entry.actuator(
                owner=self.__owner,
                context=context,
                value=value
            )
        else:
            return self.__entry.actuator


class MenuEntry:
    def __init__(self, type, title, value=None, actuator=None):
        self.type = type
        self.title = title
        self.value = value
        self.actuator = actuator
