class StaticActuator:
    def __init__(self, content, modifiers=[], targets=[]):
        self.__content = content
        self.__modifiers = modifiers
        self.__targets = targets

    def content(self, context):
        return self.__content

    def action(self, context, action, value=None):
        for modifier in self.__modifiers:
            modifier(context, action, value)
        actuator = next(
            (
                target
                for (match, target)
                in self.__targets
                if match(context, action, value)
            ),
            None
        )
        return actuator
