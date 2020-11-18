from .context import Context
from datetime import datetime
import math


class GameRunner:
    def __init__(self, actuator, error_views=[]):
        self.__actuators = []
        self.__errors = error_views
        self.set_actuator(actuator)

    def version(self):
        return "0.0.1"

    def content(self):
        actuator = self.actuator()
        try:
            content = actuator.content(self.__context)
            return content
        except Exception as e:
            print("Get content failed")
            print(e)
            return self.get_error_content("content-error")

    def get_error_content(self, id):
        return next((
            e
            for e in iter(self.__errors)
            if e.get("id", None) == id
        ), None)

    def player(self):
        player = self.__context.player
        if player:
            return player.content()
        return None

    def game(self):
        game = self.__context.game
        if game:
            return {
                "time": str(datetime.fromtimestamp(math.floor(game.time)))
            }
        return None

    def actuator(self):
        return self.__actuators[-1]

    def set_actuator(self, actuator):
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
        self.__context = Context(self.__actuators)

    def action(self, action_data):
        try:
            action = self.__context.get_obj(action_data["id"])
            actuator = self.actuator()
            selectedActuator = actuator.action(
                self.__context,
                action if action else action_data
            )
            self.set_actuator(selectedActuator)
        except Exception as e:
            print(e)
