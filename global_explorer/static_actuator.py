class StaticActuator:
    def __init__(self, content, modifiers=None):
        self.__content = content
        self.__modifiers = modifiers
        self.parent = None
        self.game = None

    def set_parent(self, parent):
        self.parent = parent

    def set_game(self, game):
        self.game = game

    def content(self):
        return self.__content

    @property
    def player(self):
        if self.game:
            return self.game.player
        return None

    def action(self, action):
        if self.__modifiers and self.parent:
            for modifier in self.__modifiers:
                modifier(self.parent, action)
        return self.parent
