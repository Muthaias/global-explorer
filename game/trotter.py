class TrotterState:
    def __init__(
        self,
        player,
        trace=None,
        time=None,
    ):
        self.__player = player
        self.__time = time if time is not None else 0
        self.__trace = trace if trace is not None else []

    @property
    def time(self):
        return self.__time

    @property
    def trace(self):
        return iter(self.__trace)

    @property
    def player(self):
        return self.__player

    def pass_time(self, seconds=0):
        self.__time += seconds

    def add_trace(self, node):
        self.__trace.append(node)
