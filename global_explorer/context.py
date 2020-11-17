class Context:
    def __init__(self, origin):
        self.__origin = origin
        self.__game = None
        self.__palyer = None

    def set_game(self, game):
        self.__game = game

    def set_player(self, player):
        self.__player = player

    @property
    def game(self):
        return self.__game

    @property
    def player(self):
        return self.__player


class ChainedContext:
    def __init__(self, contexts=[]):
        self.__contexts = contexts

    @property
    def game(self):
        return next(
            (
                context.game
                for context in self.__contexts
                if hasattr(context, "game")
            ),
            None
        )

    @property
    def player(self):
        return next(
            (
                context.player
                for context in self.__contexts
                if hasattr(context, "player")
            ),
            None
        )
