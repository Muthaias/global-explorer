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
        node = game.node
        type = self.obj_attr(node, "type")
        if type == "hub":
            return self.content_from_map(game, context)
        elif type == "visit":
            return self.content_from_info(game, context)
        else:
            return self.content_from_map(game, context)

    def content_from_map(self, game, context):
        node = game.node
        return {
            "type": "map",
            "title": self.title(node),
            "background": node.descriptor.background,
            "locations": [],
            "actions": self.action_content(game, context)
        }

    def content_from_info(self, game, context):
        node = game.node
        d = node.descriptor
        return {
            "type": "info",
            "title": self.title(node),
            "markdown": d.description if d.description else "",
            "background": d.background,
            "titleImage": d.title_image if d.title_image else "",
            "actions": self.action_content(game, context)
        }
    
    def action_content(self, game, context):
        node = game.node
        return [
            {
                "title": self.title(action),
                "type": "navigate",
                "id": context.get_id(action),
                "enabled": action.match(node, game)
            }
            for action in node.actions
        ]

    def title(self, obj):
        return self.obj_attr(obj, "title", "%s: %s" % (
            obj.__class__.__name__,
            hex(id(obj))
        ))
    
    def obj_attr(self, obj, attr_id, default=None):
        return (
            getattr(obj.descriptor, attr_id)
            if obj.descriptor
            is not None
            else default
        )

    def default_content(self, context):
        raise ValueError("Context has no Game object")
