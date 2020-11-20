from uuid import uuid4


class Context:
    def __init__(self, contexts=[]):
        self.__contexts = contexts
        self.__object_dict = {}

    def chained_attr(self, id):
        return next(
            (
                getattr(context, id)
                for context in reversed(self.__contexts)
                if hasattr(context, id)
            ),
            None
        )

    def get_id(self, obj):
        id = self.__object_dict.get(obj, None)
        if not id:
            id = str(uuid4())
            self.__object_dict[id] = obj
            self.__object_dict[obj] = id
        return id

    def get_obj(self, id):
        return self.__object_dict.get(id, None)

    @property
    def location(self):
        return self.chained_attr("location")

    @property
    def game(self):
        return self.chained_attr("game")

    @property
    def player(self):
        return self.chained_attr("player")
