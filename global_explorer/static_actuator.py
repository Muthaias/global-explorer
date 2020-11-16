class StaticActuator:
    def __init__(self, content, modifier = None):
        self.__content = content
        self.__modifier = modifier
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
        if self.__modifier and self.parent:
            self.__modifier(self.parent)
        return self.parent