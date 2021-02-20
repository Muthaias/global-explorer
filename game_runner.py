from time import time
from presentation import (
    Menu,
    MenuEntry,
    StaticActuator,
    GameActuator,
    GameRunner,
    NodeActuator,
)
from game.game import Game
from game.trotter import TrotterState, Player, Account, Transaction
import game_maps


def create_game_runner(node_manager, previous_game):
    def new_game_menu(
        context=None,
        owner=None,
        value=None
    ):
        name = value if value else "Dirk Smallwood"
        initial_funds = Transaction(1000)
        player = Player(
            name=name,
            account=Account([initial_funds]),
            skills=[]
        )

        games = [
            (
                entry_point.descriptor.title,
                Game.from_node(
                    node=entry_point,
                    state=TrotterState(
                        player=player,
                        time=time(),
                    ),
                )
            )
            for entry_point in node_manager.entry_points
        ]
        return Menu(
            [
                MenuEntry(
                    type="navigate",
                    title=title,
                    actuator=GameActuator(
                        game=game,
                        actuator=NodeActuator()
                    )
                )
                for title, game in games
            ],
            "https://images.unsplash.com/photo-1554123168-b400f9c806ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
            allow_back=True,
            title="Select Location",
            description="Where in the world would you like to start?"
        )

    main_menu = Menu(
        [
            MenuEntry(
                type="input",
                title="New game",
                value="Unknown Player",
                actuator=new_game_menu
            ),
            *([
                MenuEntry(
                    type="navigate",
                    title="Load game",
                    actuator=GameActuator(
                        game=previous_game,
                        actuator=NodeActuator()
                    )
                )
            ] if previous_game else []),
        ],
        "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80",
        title="Global Explorer",
        description="Welcome to Global Explorer. The game where you travel the world and learn about professions by engaging and doing things yourself."
    )

    api = GameRunner(
        actuator=main_menu,
        error_views=game_maps.error_views
    )
    return api
