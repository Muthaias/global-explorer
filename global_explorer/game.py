class Game:
    def __init__(self, player, maps, currentMap=None):
        self.maps = maps
        self.currentMap = (
            currentMap
            if currentMap is not None else self.maps[0]
        )
        self.player = player

    def content(self, id_generator):
        return {
            "type": "map",
            "title": self.currentMap.title,
            "background": self.currentMap.background,
            "locations": [
                {
                    "title": location.title,
                    "action": {
                        "type": "navigate",
                        "id": id_generator(location)
                    },
                    "position": location.position,
                }
                for location in self.currentMap.locations
            ]
        }

    def action(self, context, action):
        location = next(
            (
                loc for loc in self.currentMap.locations
                if loc is action
            ),
            None
        )
        if location and location.actuator:
            return location.actuator
        return self


class GameMap:
    def __init__(self, title, locations, background):
        self.title = title
        self.locations = locations
        self.background = background


class GameLocation:
    def __init__(self, title, position, actuator=None):
        self.title = title
        self.position = position
        self.actuator = actuator
