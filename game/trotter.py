from time import time
from datetime import datetime

from .game import (
    Game,
    Node,
    Action,
)
from .actions import (
    combine_actions,
    pass_time,
    step_into_random,
    step_into,
    step,
    add_trace,
    to_seconds,
    branch,
)
from .load_node_data import load_nodes


class TrotterState:
    def __init__(
        self,
        player,
        trace=None,
        time=None,
    ):
        self.__player = player
        self.__time = time if time is not None else 0
        self.__trace = trace if trace is not None else []

    @property
    def time(self):
        return self.__time

    @property
    def trace(self):
        return iter(self.__trace)

    @property
    def player(self):
        return self.__player

    def pass_time(self, seconds=0):
        self.__time += seconds

    def add_trace(self, node):
        self.__trace.append(node)


def time_is_more(t):
    def _time_is_more(node, game):
        print(
            datetime.fromtimestamp(game.state.time),
            datetime.fromtimestamp(t)
        )
        return game.state.time > t
    return _time_is_more


def quick_setup():
    game_start = time()
    on_action = combine_actions([
        add_trace,
        step
    ])
    dict = {}
    to_a = Action(apply=combine_actions([
        add_trace,
        pass_time(to_seconds(hours=1)),
        step_into(["a"], dict)
    ]))
    to_b = Action(apply=combine_actions([
        add_trace,
        pass_time(to_seconds(hours=1)),
        step_into(["b"], dict)
    ]))
    to_c = Action(apply=combine_actions([
        add_trace,
        pass_time(to_seconds(hours=1)),
        step_into(["c"], dict)
    ]))
    dict["a"] = Node(
        actions=[
            to_b,
            to_c,
        ]
    )
    dict["b"] = Node(
        actions=[
            Action(
                apply=branch(
                    time_is_more(game_start + 2 * 3600),
                    step_into(["c"], dict),
                    step_into_random(["b0", "b1", "b2"], 2, dict),
                )
            ),
            to_a,
            to_c,
        ],
        on_action=combine_actions([
            add_trace,
            pass_time(to_seconds(hours=1)),
        ])
    )
    dict["b0"] = Node(
        actions=[
            Action(apply=combine_actions([
                pass_time(to_seconds(minutes=10)),
            ])),
        ],
        on_action=on_action
    )
    dict["b1"] = Node(
        actions=[
            Action(apply=combine_actions([
                pass_time(to_seconds(minutes=10)),
            ])),
        ],
        on_action=on_action
    )
    dict["b2"] = Node(
        actions=[
            Action(apply=combine_actions([
                pass_time(to_seconds(minutes=10)),
            ])),
        ],
        on_action=on_action
    )
    dict["c"] = Node(
        actions=[
            to_a,
            to_b,
        ]
    )
    reverse_dict = {
        node: key for key, node in dict.items()
    }
    trotter = TrotterState(
        player={},
        time=game_start,
        trace=[]
    )
    game = Game(
        state=trotter,
        stack=[[dict["a"]]]
    )
    return (game, reverse_dict)


def run_nav_demo():
    loaded_nodes = load_nodes([
        "data/defaults.yaml",
        "data/uppsala.yaml"
    ])
    print(loaded_nodes)

    (game, reverse_dict) = quick_setup()

    for i in range(20):
        node = game.node
        action = node.actions[0]
        id = reverse_dict.get(node, None)
        print("step", id, node, datetime.fromtimestamp(game.state.time))
        if action:
            game.handle_action(action)

    for node in game.state.trace:
        id = reverse_dict.get(node, None)
        print(id, node)
