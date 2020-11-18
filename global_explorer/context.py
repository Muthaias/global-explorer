class ChainedContext:
    def __init__(self, contexts=[]):
        self.__contexts = contexts

    def chained_attr(self, id):
        return next(
            (
                getattr(context, id)
                for context in reversed(self.__contexts)
                if hasattr(context, id)
            ),
            None
        )

    @property
    def location(self):
        return self.chained_attr("location")

    @property
    def scope(self):
        return self.chained_attr("scope")

    @property
    def game(self):
        return self.chained_attr("game")

    @property
    def player(self):
        return self.chained_attr("player")
