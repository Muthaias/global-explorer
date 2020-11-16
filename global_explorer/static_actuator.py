class StaticActator:
    def __init__(self, content):
        self.__content = content
        self.parent = None
    
    def set_parent(self, parent):
        self.parent = parent

    def content(self):
        return self.__content
    
    def action(self, action):
        print(action)
        return self.parent