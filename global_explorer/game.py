class Game:
    def __init__(self, world, player, time, location):
        self.time = time
        self.world = world
        self.player = player
        self.__location = location

    def pass_time(self, days=0, hours=0, seconds=0):
        self.time += seconds + hours * 3600 + days * 24 * 3600

    def set_location(self, location):
        self.__location = location

    @property
    def location(self):
        return self.__location

    @property
    def sub_locations(self):
        for location in self.world.locations_by_parent(self.location):
            if location.match(self):
                yield location


class GameWorld:
    def location_by_id(self, id):
        pass

    def locations_by_type(self, type):
        pass

    def locations_by_parent(self, parent):
        pass

    def locations_by_link(self, origin):
        pass


class StaticGameWorld(GameWorld):
    def __init__(self, locations, links=[]):
        self.__locations = locations
        self.__links = links

    def location_by_id(self, id):
        return next(
            (location for location in self.__locations if location.id == id),
            None
        )

    def locations_by_type(self, type):
        for location in self.__locations:
            if location.type == type:
                yield location

    def locations_by_parent(self, parent):
        for location in self.__locations:
            if location.parent is parent:
                yield location

    def locations_by_link(self, origin):
        for (loc_a, loc_b) in self.__locations:
            if loc_a is origin or loc_b is origin:
                yield loc_a if loc_a is not origin else loc_b


class GameAction:
    def __init__(self, title, update=None, match=None):
        self.title = title
        self.__update = update
        self.__match = match

    def match(self, game):
        return self.__match(game) if self.__match else True

    def update(self, game):
        return self.__update(game) if self.__update else None


class GameLocation(GameAction):
    def __init__(
        self,
        title,
        position,
        background=None,
        title_image=None,
        actions=None,
        parent=None,
        actuator=None,
        description=None,
        match=None,
        update=None,
    ):
        super().__init__(
            title=title,
            match=match,
            update=update
        )
        self.title = title
        self.description = description
        self.background = background
        self.title_image = title_image

        self.position = position
        self.actions = actions if actions is not None else [
            GameAction(
                title="Leave",
            )
        ]
        self.actuator = actuator
        self.parent = parent

