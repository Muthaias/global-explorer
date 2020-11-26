import random
import datetime
from .trotter import Transaction, Skill


def get_nodes(ids_or_func, dict):
    ids = ids_or_func if isinstance(ids_or_func, list) else ids_or_func()
    nodes = [dict[id] for id in ids if id in dict]
    return nodes


def step_into(ids_or_func, dict):
    def _step_into(node, game):
        nodes = get_nodes(ids_or_func, dict)
        if len(nodes) > 0:
            game.step_into(nodes)
    return _step_into


def step_into_random(ids, count, dict):
    def _step_into_random(node, game):
        random_ids = random.sample(ids, k=count)
        step_into(random_ids, dict)(node, game)
    return _step_into_random


def select_by_tags(tags, dict, count=0, ex_tags=[]):
    ids = [
        id
        for id, node in dict.items()
        if False not in {
            (tag in node.descriptor.tags)
            for tag in tags
        }
        and True not in {
            (ex_tag in node.descriptor.tags)
            for ex_tag in ex_tags
        }
    ]
    count = (
        min(count, len(ids))
        if count > 0 else len(ids)
    )
    return ids[0:count]


def require_skill(id, value):
    def _require_skill(node, game):
        return game.state.player.verify_skill(id, value)
    return _require_skill


def require_funds(value):
    def _require_funds(node, game):
        return game.state.player.account.balance >= value
    return _require_funds


def require_time(iso_time_a, iso_time_b, wdays=None):
    def _require_time(node, game):
        current_dt = datetime.datetime.fromtimestamp(game.state.time)
        time = current_dt.time()
        wday = current_dt.weekday()
        time_a = datetime.time.fromisoformat(iso_time_a)
        time_b = datetime.time.fromisoformat(iso_time_b)

        if (
            wdays is None or
            (wday >= wdays[0] and wday <= wdays[1])
        ):
            if time >= time_a and time <= time_b:
                return True
        return False
    return _require_time


def add_skill(id, value, description=None):
    def _add_skill(node, game):
        skill = Skill(
            description=description,
            skill_points={
                id: value
            }
        )
        game.state.player.add_skill(skill)
    return _add_skill


def transfer(ids_or_func, dict):
    def _transfer(node, game):
        nodes = get_nodes(ids_or_func, dict)
        if len(nodes) > 0:
            game.transfer(nodes)
    return _transfer


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
