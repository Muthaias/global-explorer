from global_explorer import (
    GameAction,
    StaticGameWorld,
    StaticActuator,
    Transaction,
    LocationVisit,
    LocationHub,
)
from global_explorer.load_data import load_locations, load_yaml


def action_id_condition(id, modifier):
    def conditional_modifier(context, action):
        if action["id"] == id:
            modifier(context, action)
    return conditional_modifier


def action_id_target(id, actuator):
    def match(context, action):
        return action["id"] == id
    return (match, actuator)


def add_cash_action(amount):
    def modifier(game):
        game.player.account.add_transaction(Transaction(amount))
    return modifier


def go_back_action(context, action):
    game = context.game
    if game and game.location.parent:
        game.location = game.location.parent


def enter_actuator_action(actuator):
    def action(game):
        return actuator
    return action


def pass_time_action(seconds=0, hours=0, days=0):
    def action(game):
        game.pass_time(
            seconds=seconds,
            hours=hours,
            days=days
        )
    return action


def combine_actions(actions):
    def action(game):
        actuator = None
        for a in actions:
            result = a(game)
            actuator = result if result else actuator
        return actuator
    return action


engineering = StaticActuator(
    {
        "type": "info",
        "title": "Engineering",
        "markdown": "",
        "titleImage": "https://images.unsplash.com/photo-1581094017399-34c4fb48c65b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
        "background": "https://images.unsplash.com/photo-1580810709956-ea1561ce6bcb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1875&q=80",
        "actions": [
            {
                "type": "navigate",
                "title": "Leave",
                "id": "leave"
            }
        ],
    }
)

actions_dict = {
    "polacksbacken": [
        GameAction(
            title="Study engineering",
            update=enter_actuator_action(
                engineering
            )
        ),
        GameAction(
            title="Study math"
        ),
        GameAction(
            title="Study physics"
        ),
        GameAction(
            title="Study computer science"
        ),
        GameAction(
            title="Leave"
        )
    ],
    "ofvandahls": [
        GameAction(
            title="Have a fika",
            update=combine_actions([
                add_cash_action(-10),
                pass_time_action(hours=2)
            ])
        ),
        GameAction(
            title="Have a coffee",
            update=combine_actions([
                add_cash_action(-5),
                pass_time_action(hours=1)
            ])
        ),
        GameAction(
            title="Leave",
        )
    ]
}

match_dict = {
    "studentvagen": lambda game: game.player.account.balance < 1000
}

update_dict = {
    "flogsta": add_cash_action(10)
}

actuator_dict = {
    "polacksbacken": LocationVisit(),
    "ofvandahls": LocationVisit(),
}

loaded_locations = load_locations([
    "data/defaults.yaml",
    "data/stockholm.yaml",
    "data/uppsala.yaml"
])

for location in loaded_locations:
    actuator = actuator_dict.get(location.id, LocationHub())
    actions = actions_dict.get(location.id, None)
    update = update_dict.get(location.id, None)
    match = match_dict.get(location.id, None)

    location.actuator = actuator
    if update:
        location.update = update
    if match:
        location.match = match
    if actions:
        location.actions = actions

cities = [
    location
    for location in loaded_locations
    if location.id == "uppsala" or location.id == "stockholm"
]

world = StaticGameWorld(
    locations=loaded_locations
)

error_views = load_yaml("data/error_views.yaml").get("errors", [])
