class StaticActator:
    def __init__(self, content):
        self.__content = content
    
    def set_parent(self, parent):
        pass

    def content(self):
        return self.__content
    
    def action(self, action):
        print(action)