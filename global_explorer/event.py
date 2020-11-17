class Event:
    def __init__(self, context, action):
        self.__context = context
        self.__action = action
        self.__should_propagate = True
        self.__next_actuator = None

    def set_next_actuator(self, actuator):
        self.__next_actuator = actuator

    def stop_propagation(self):
        self.__should_propagate = False

    @property
    def should_propagate(self):
        return self.__should_propagate

    @property
    def next_actuator(self):
        return self.__next_actuator
