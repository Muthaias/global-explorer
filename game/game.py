class Game:
    def __init__(self, state, stack=[]):
        self.__stack = []
        for sequence in stack:
            self.__stack.append(Sequence(iter(sequence)))
        self.__state = state

    def step_into(self, sequence):
        self.__stack.append(Sequence(iter(sequence)))

    def step_out(self):
        self.node.on_exit(self)
        del self.__stack[-1]
        self.node.on_enter(self)

    def step(self):
        self.node.on_exit(self)
        try:
            next(self.__stack[-1])
        except StopIteration:
            del self.__stack[-1]
        self.node.on_enter(self)

    @property
    def state(self):
        return self.__state

    @property
    def node(self):
        return self.__stack[-1].current

    def handle_action(self, action):
        node = self.node
        if node:
            node.handle_action(self, action)


class Sequence:
    def __init__(self, iterator):
        self.__iterator = iterator
        self.__current = None
        self.__next__()

    def __iter__(self):
        self

    def __next__(self):
        element = self.__current
        self.__current = next(self.__iterator)
        return element

    @property
    def current(self):
        return self.__current


class Node:
    def __init__(
        self,
        actions=None,
        on_enter=None,
        on_action=None,
        on_exit=None
    ):
        self.__actions = actions if actions is not None else []
        self.__on_enter = on_enter
        self.__on_action = on_action
        self.__on_exit = on_exit

    @property
    def actions(self):
        return self.__actions

    def handle_action(self, game, action):
        if action in self.__actions and action.match(self, game):
            if self.__on_action:
                self.__on_action(self, game)
            action.apply(self, game)

    def on_enter(self, game):
        if self.__on_enter:
            self.__on_enter(self, game)

    def on_exit(self, game):
        if self.__on_exit:
            self.__on_exit(self, game)


class Action:
    def __init__(self, match=None, apply=None):
        self.__apply = apply
        self.__match = match

    def match(self, node, game):
        return self.__match(node, game) if self.__match else True

    def apply(self, node, game):
        if self.__apply:
            self.__apply(node, game)
