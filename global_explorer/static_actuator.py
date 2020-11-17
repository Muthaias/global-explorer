class StaticActuator:
    def __init__(self, content, modifiers=None):
        self.__content = content
        self.__modifiers = modifiers

    def content(self):
        return self.__content

    def action(self, context, action):
        if self.__modifiers:
            for modifier in self.__modifiers:
                modifier(context, action)
        return None
