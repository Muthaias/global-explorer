class GameActuator:
    def __init__(self, game, actuator):
        self.__game = game
        self.__actuator = actuator

    @property
    def game(self):
        return self.__game

    @property
    def player(self):
        return self.game.player

    @property
    def location(self):
        return self.game.location

    @property
    def actuator(self):
        location = self.game.location
        return location.actuator if location.actuator else self.__actuator

    def content(self, context):
        return self.actuator.content(context)

    def action(self, context, action):
        actuator = self.actuator.action(context, action)
        return actuator if actuator else self
