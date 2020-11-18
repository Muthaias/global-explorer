class LocationHub:
    def content(self, context, id_generator):
        game = context.game
        return (
            self.content_from_game(game, id_generator)
            if game
            else self.default_content(context, id_generator)
        )

    def action(self, context, action):
        game = context.game
        if game:
            location = self.location_from_action(context, action)
            if location:
                game.location = location

            if hasattr(action, "update"):
                return action.update(game)
        return None

    def content_from_game(self, game, id_generator):
        return {
            "type": "map",
            "title": game.location.title,
            "background": game.location.background,
            "locations": [
                {
                    "title": location.title,
                    "action": {
                        "type": "navigate",
                        "id": id_generator(location)
                    },
                    "position": location.position,
                }
                for location in game.sub_locations
            ],
            "actions": [
                {
                    "title": action.title,
                    "type": "navigate",
                    "id": id_generator(action)
                }
                for action in game.location.actions
                if action.match(game)
            ]
        }

    def default_content(self, context, id_generator):
        return {
            "type": "menu",
            "title": "Nothing for you here",
            "background": "https://images.unsplash.com/photo-1487803556724-cb9f0b8151d1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1858&q=80",
            "actions": [{
                "type": "exit",
                "id": id_generator("exit"),
                "title": "Go back",
            }],
        }

    def location_from_action(self, context, action):
        game = context.game
        return next(
            (
                loc for loc in game.sub_locations
                if loc is action
            ),
            game.location.parent
        ) if game else None


class LocationVisit(LocationHub):
    def content_from_game(self, game, id_generator):
        location = game.location
        return {
            "type": "info",
            "title": location.title,
            "markdown": location.description if location.description else "",
            "background": location.background,
            "titleImage": location.title_image if location.title_image else "",
            "actions": [
                {
                    "title": action.title,
                    "type": "navigate",
                    "id": id_generator(action)
                }
                for action in location.actions
                if action.match(game)
            ]
        }

    def location_from_action(self, context, action):
        game = context.game
        if game:
            return game.location.parent
        return None

    def action(self, context, action):
        game = context.game
        return LocationHub.action(self, context, action)
