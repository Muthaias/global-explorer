from game import (
    Game,
    Node,
    Action,
)
from actions import (
    combine_actions,
    pass_time,
    step_into,
    step_out,
    step,
    add_trace,
    to_seconds,
)
from time import time
from datetime import datetime


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


class NodeBuilder:
    def __init__(self):
        self.__dict = {}

    def create_location(self, location_data):
        node = Node()
        self.__dict[node] = location_data
        return node

    def create_action(self, action_data):
        action = Action()
        self.__dict[action] = action_data
        return action

    def get_location_data(self, node):
        return self.__dict.get(node, None)

    def get_action_data(self, action):
        return self.__dict.get(action, None)


if __name__ == "__main__":
    dict = {}
    dict["a"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(hours=1)),
                step_into(["b"], dict)
            ])),
        ]
    )
    dict["b"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(hours=1)),
                step_into(["b0", "b1", "b2"], dict)
            ])),
        ]
    )
    dict["b0"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(minutes=10)),
                step
            ])),
        ]
    )
    dict["b1"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(minutes=10)),
                step
            ])),
        ]
    )
    dict["b2"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(minutes=10)),
                step
            ])),
        ]
    )
    dict["c"] = Node(
        actions=[
            Action(apply=combine_actions([
                add_trace,
                pass_time(to_seconds(hours=1)),
                step_into(["a"], dict)
            ])),
        ]
    )
    reverse_dict = {
        node: key for key, node in dict.items()
    }
    trotter = TrotterState(
        player={},
        time=time(),
        trace=[]
    )
    game = Game(
        state=trotter,
        stack=[[dict["a"]]]
    )

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
