def step_into(ids, dict):
    def _step_into(node, game):
        nodes = [dict[id] for id in ids if id in dict]
        if len(nodes) > 0:
            game.step_into(nodes)
    return _step_into


def step_out(node, game):
    game.step_out()


def add_trace(node, game):
    game.state.add_trace(node)


def step(node, game):
    game.step()


def combine_actions(actions):
    def _combine_actions(node, game):
        for action in actions:
            action(node, game)
    return _combine_actions


def pass_time(seconds=0):
    def _pass_time(node, game):
        game.state.pass_time(seconds)

    return _pass_time


def to_seconds(days=0, hours=0, minutes=0, seconds=0):
    return days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds