class Game:
    def __init__(self, state, stack=[]):
        self.__stack = []
        for sequence in stack:
            self.step_into(sequence)
        self.__state = state

    def step_into(self, sequence):
        self.__stack.append([node for node in sequence])

    def step_out(self):
        self.node.on_exit(self)
        del self.__stack[-1]
        self.node.on_enter(self)

    def transfer(self, sequence):
        self.node.on_exit(self)
        if len(self.__stack) > 0:
            del self.__stack[-1]
        self.step_into(sequence)
        self.node.on_enter(self)

    def step(self):
        self.node.on_exit(self)
        self.__stack[-1] = self.__stack[-1][1:len(self.__stack[-1])]
        if len(self.__stack[-1]) == 0:
            del self.__stack[-1]
        self.node.on_enter(self)

    @property
    def state(self):
        return self.__state

    @property
    def node(self):
        return self.__stack[-1][0]

    def handle_action(self, action, value=None):
        node = self.node
        if node:
            node.handle_action(self, action, value)

    @staticmethod
    def from_node(node, state=None):
        return Game(
            stack=[[node]],
            state=state,
        )


class Node:
    def __init__(
        self,
        actions=None,
        on_enter=None,
        on_action=None,
        on_exit=None,
        descriptor=None
    ):
        self.__actions = actions if actions is not None else []
        self.__on_enter = on_enter
        self.__on_action = on_action
        self.__on_exit = on_exit
        self.__descriptor = descriptor

    def set_actions(self, actions):
        self.__actions = actions

    @property
    def actions(self):
        return self.__actions

    @property
    def descriptor(self):
        return self.__descriptor

    def handle_action(self, game, action, value=None):
        if action in self.__actions and action.match(self, game):
            if self.__on_action:
                self.__on_action(self, game)
            action.apply(self, game, value)

    def on_enter(self, game):
        if self.__on_enter:
            self.__on_enter(self, game)

    def on_exit(self, game):
        if self.__on_exit:
            self.__on_exit(self, game)


class Action:
    def __init__(self, match=None, apply=None, descriptor=None):
        self.__apply = apply
        self.__match = match
        self.__descriptor = descriptor

    @property
    def descriptor(self):
        return self.__descriptor

    def match(self, node, game):
        return self.__match(node, game) if self.__match else True

    def apply(self, node, game, value):
        if self.__apply:
            self.__apply(node, game, value)
