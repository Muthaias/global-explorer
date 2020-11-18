
import webview
from global_explorer import (
    Menu,
    MenuEntry,
    StaticActuator,
    GameActuator,
    Player,
    Account,
    Transaction,
    GameRunner,
    Game,
    LocationHub
)
from time import time
import game_maps

noop = StaticActuator({
    "type": "menu",
    "background": "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80",
    "actions": [
        {
            "type": "navigate",
            "title": "New game",
            "id": "new-game"
        },
        {
            "type": "navigate",
            "title": "Load game",
            "id": "load-game"
        }
    ]
})

info = StaticActuator({
    "type": "info",
    "title": "Hello World!",
    "markdown": "This is a test of the info type content",
    "titleImage": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1347&q=80",
    "background": "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80",
    "actions": [{
        "type": "navigate",
        "title": "Finish",
        "id": "finish"
    }],
})

initial_funds = Transaction(1000)

player = Player(
    name="Rick Pickle",
    account=Account([initial_funds]),
    skills=[]
)

sthlm = GameActuator(
    game=Game(
        world=game_maps.world,
        location=game_maps.stockholm,
        time=time(),
        player=player,
    ),
    actuator=LocationHub()
)
upsl = GameActuator(
    game=Game(
        world=game_maps.world,
        location=game_maps.uppsala,
        time=time(),
        player=player,
    ),
    actuator=LocationHub()
)
new_game_menu = Menu(
    [
        MenuEntry(
            type="navigate",
            title="Stockholm",
            actuator=sthlm
        ),
        MenuEntry(
            type="navigate",
            title="Uppsala",
            actuator=upsl
        ),
        MenuEntry(
            type="navigate",
            title="Göteborg",
            actuator=noop
        ),
        MenuEntry(
            type="navigate",
            title="Malmö",
            actuator=noop
        ),
        MenuEntry(
            type="navigate",
            title="Kiruna",
            actuator=noop
        )
    ],
    "https://images.unsplash.com/photo-1554123168-b400f9c806ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    allow_back=True
)

main_menu = Menu(
    [
        MenuEntry(
            type="navigate",
            title="New game",
            actuator=new_game_menu
        ),
        MenuEntry(
            type="navigate",
            title="Load game",
            actuator=info
        ),
        MenuEntry(
            type="navigate",
            title="Settings",
            actuator=noop
        ),
        MenuEntry(
            type="navigate",
            title="Credits",
            actuator=noop
        ),
    ],
    "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80"
)

api = GameRunner(main_menu)
webview.create_window("Global Explorer", "assets/index.html", js_api=api)
webview.start(debug=True)
