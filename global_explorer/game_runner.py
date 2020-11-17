from .context import ChainedContext


class GameRunner:
    def __init__(self, actuator):
        self.__actuators = []
        self.set_actuator(actuator)

    def version(self):
        return "0.0.1"

    def content(self):
        actuator = self.actuator()
        try:
            content = actuator.content()
            return content
        except Exception as e:
            print("Get content failed")
            print(e)

    def player(self):
        player = self.__context.player
        if player:
            return player.content()
        return None

    def actuator(self):
        return self.__actuators[-1]

    def set_actuator(self, actuator):
        actuatorIndex = next(
            (
                i for i, e in enumerate(self.__actuators)
                if e is actuator
            ),
            None
        )
        if actuatorIndex is None:
            self.__actuators.append(actuator)
        else:
            self.__actuators = self.__actuators[
                0:actuatorIndex + 1
            ]
        self.__context = ChainedContext(reversed(self.__actuators))

    def action(self, action):
        actuator = self.actuator()
        try:
            selectedActuator = actuator.action(action)
            self.set_actuator(selectedActuator)
        except Exception as e:
            print(e)
