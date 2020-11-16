class GameRunner:
    def __init__(self, actuator):
        self.actuators = [actuator]

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
        actuator = self.actuator()
        if hasattr(actuator, "player") and actuator.player:
            return actuator.player.content()
        return None

    def actuator(self):
        return self.actuators[-1]

    def action(self, action):
        actuator = self.actuator()
        try:
            selectedActuator = actuator.action(action)
            if selectedActuator:
                existingActuatorIndex = next(
                    (
                        i for i, e in enumerate(self.actuators)
                        if e is selectedActuator
                    ),
                    None
                )
                if existingActuatorIndex is None:
                    self.actuators.append(selectedActuator)
                else:
                    self.actuators = self.actuators[
                        0:existingActuatorIndex + 1
                    ]
                print(selectedActuator, existingActuatorIndex, self.actuators)
        except Exception as e:
            print(e)
