class StaticActuator:
    def __init__(self, content, modifiers=[], targets=[]):
        self.__content = content
        self.__modifiers = modifiers
        self.__targets = targets

    def content(self, context):
        return self.__content

    def action(self, context, action):
        for modifier in self.__modifiers:
            modifier(context, action)
        actuator = next(
            (
                target
                for (match, target)
                in self.__targets
                if match(context, action)
            ),
            None
        )
        return actuator
