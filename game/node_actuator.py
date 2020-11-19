class NodeActuator:
    def content(self, context):
        game = context.game
        return (
            self.content_from_game(game, context)
            if game
            else self.default_content(context)
        )

    def action(self, context, action):
        game = context.game
        if game:
            game.handle_action(action)

        return self

    def content_from_game(self, game, context):
        print(game)
        node = game.node
        return {
            "type": "map",
            "title": "%s: %s" % (
                node.__class__.__name__,
                hex(id(node))
            ),
            "background": "",
            "locations": [],
            "actions": [
                {
                    "title": "%s: %s" % (
                        action.__class__.__name__,
                        hex(id(action))
                    ),
                    "type": "navigate",
                    "id": context.get_id(action)
                }
                for action in node.actions
                if action.match(node, game)
            ]
        }

    def default_content(self, context):
        raise ValueError("Context has no Game object")
