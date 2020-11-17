from .context import ChainedContext
from uuid import uuid4


class GameRunner:
    def __init__(self, actuator):
        self.__actuators = []
        self.set_actuator(actuator)

    def version(self):
        return "0.0.1"

    def content(self):
        actuator = self.actuator()
        action_map = {}

        def id_generator(action):
            id = str(uuid4())
            action_map[id] = action
            return id

        try:
            content = actuator.content(id_generator)
            self.__action_map = action_map
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
        actuator = actuator if actuator else self.__context.scope
        if actuator:
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
        else:
            self.__actuators = self.__actuators[
                0:len(self.__actuators) - 1
            ]
        self.__context = ChainedContext(self.__actuators)

    def action(self, action_data):
        action = self.__action_map.get(action_data["id"], None)
        actuator = self.actuator()
        try:
            selectedActuator = actuator.action(
                self.__context,
                action if action else action_data
            )
            self.set_actuator(selectedActuator)
        except Exception as e:
            print(e)
