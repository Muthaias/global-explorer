class StaticActuator:
    def __init__(self, content, modifier = None):
        self.__content = content
        self.__modifier = modifier
        self.parent = None
    
    def set_parent(self, parent):
        self.parent = parent

    def content(self):
        return self.__content

    @property
    def player(self):
        if hasattr(self.parent, "player"):
            return self.parent.player
        return None
    
    def action(self, action):
        if self.__modifier and self.parent:
            self.__modifier(self.parent)
        return self.parent