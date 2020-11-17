class Event:
    def __init__(self, context, action):
        self.__context = context
        self.__action = action
        self.__should_propagate = True

    def stop_propagation(self):
        self.__should_propagate = False

    @property
    def should_propagate(self):
        return self.__should_propagate
