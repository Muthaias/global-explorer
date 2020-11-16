from uuid import uuid4
from .player import Transaction

class Game:
    def __init__(self, player, maps, currentMap = None):
        self.maps = maps
        self.currentMap = currentMap if currentMap != None else self.maps[0]
        self.player = player
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def content(self):
        return {
            "type": "map",
            "title": self.currentMap.title,
            "background": self.currentMap.background,
            "locations": [
                {
                    "title": location.title,
                    "action": {
                        "type": "navigate",
                        "id": location.id
                    },
                    "position": location.position,
                }
                for location in self.currentMap.locations
            ]
        }
    
    def action(self, action):
        location = next((l for l in self.currentMap.locations if l.id == action["id"]), None)
        if location and location.actuator:
            location.actuator.set_game(self)
            location.actuator.set_parent(self)
            return location.actuator
        return self

class GameMap:
    def __init__(self, title, locations, background):
        self.title = title
        self.locations = locations
        self.background = background

class GameLocation:
    def __init__(self, title, position, actuator = None):
        self.id = str(uuid4())
        self.title = title
        self.position = position
        self.actuator = actuator