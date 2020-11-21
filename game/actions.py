import random
from .trotter import Transaction


def step_into(ids, dict):
    def _step_into(node, game):
        nodes = [dict[id] for id in ids if id in dict]
        if len(nodes) > 0:
            game.step_into(nodes)
    return _step_into


def step_into_random(ids, count, dict):
    def _step_into_random(node, game):
        random_ids = random.sample(ids, k=count)
        step_into(random_ids, dict)(node, game)
    return _step_into_random


def select_by_tags(tags, dict, count=0):
    ids = [
        id
        for id, node in dict.items()
        if False not in ((tag in node.descriptor.tags) for tag in tags)
    ]
    count = (
        min(count, len(ids))
        if count > 0 else len(ids)
    )
    return ids[0:count]


def step_out(node, game):
    game.step_out()


def add_trace(node, game):
    game.state.add_trace(node)


def step(node, game):
    game.step()


def combine_actions(*actions):
    def _combine_actions(node, game):
        for action in actions:
            action(node, game)
    return _combine_actions


def pass_time(seconds=0):
    def _pass_time(node, game):
        game.state.pass_time(seconds)
    return _pass_time


def charge_card(amount=0, issuer=None):
    def _charge_card(node, game):
        game.state.player.account.add_transaction(
            Transaction(
                amount=-amount,
                description=issuer if issuer else "Unknown"
            )
        )
    return _charge_card


def branch(condition, a, b):
    def _branch(node, game):
        if condition(node, game):
            a(node, game)
        else:
            b(node, game)
    return _branch


def time_of_day(func, s0, s1):
    pass


def to_seconds(days=0, hours=0, minutes=0, seconds=0):
    return days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
