from global_explorer import GameLocation, GameAction, StaticGameWorld, StaticActuator, Transaction, LocationVisit


lorem_ipsum_data = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor ipsum ligula, id pulvinar risus scelerisque a. Integer eget ultricies nunc, et varius diam. Morbi eu tortor sed ipsum venenatis porttitor. Duis efficitur, neque id dignissim condimentum, mauris lacus ornare neque, at tincidunt risus massa sit amet est. Vestibulum tincidunt mi et accumsan bibendum. In porta aliquam lacus, vel aliquet erat suscipit eu. Sed at massa facilisis, mollis nibh vitae, pretium enim. Pellentesque rutrum lectus vel lorem laoreet auctor.

Nulla dignissim turpis a enim porta pretium. Aliquam ac auctor nibh. Vestibulum malesuada fringilla urna. Nam euismod efficitur turpis, a mattis tortor rhoncus eu. Ut ultrices dui eget scelerisque dignissim. Cras eu ipsum fringilla, ultricies enim mollis, cursus nisl. Nullam in metus a dolor mollis luctus sit amet egestas nunc.

Fusce sit amet maximus urna. Aenean eget lacus facilisis, sodales erat quis, varius erat. Morbi pellentesque dolor nulla, id auctor ligula elementum id. Quisque commodo felis dolor, in tempor tortor vulputate vel. Nam tincidunt porttitor cursus. Proin a diam eu metus blandit elementum ut sit amet dui. Sed auctor tristique nisl vel mattis. In at mauris ac nisi lobortis pretium eget eu velit.

Maecenas id accumsan tellus, non hendrerit magna. Donec pulvinar lacus sapien, non ornare dolor placerat vitae. Suspendisse sed semper ex. Aenean quis purus tellus. Curabitur gravida eros at euismod tincidunt. Aenean eget viverra est. Proin scelerisque mauris sagittis dui tincidunt hendrerit. Cras ac dolor urna. Donec nec bibendum neque. Etiam blandit facilisis lacus vel sodales. Proin purus ligula, dignissim ut aliquet at, sagittis ornare enim. Integer rutrum dolor at eleifend dictum.

In hac habitasse platea dictumst. Morbi quis purus enim. Sed consectetur lacinia tempor. Nulla ultrices iaculis justo eget laoreet. Nam nec ipsum consequat sapien cursus consequat. Mauris aliquet efficitur nisl, vel vulputate dui consequat at. Nullam sit amet condimentum ante, id tincidunt lorem. Sed pharetra fringilla nisl, ut viverra dolor porta at. Praesent finibus tempor diam, et venenatis velit lacinia ac. Aenean nec tincidunt ligula. Quisque commodo lorem eget velit pharetra, nec lobortis dolor commodo. Quisque lobortis elit tristique mattis gravida.
""".strip()


def add_cash_modifier(amount):
    def modifier(game):
        game.player.account.add_transaction(Transaction(amount))
    return modifier


def action_id_condition(id, modifier):
    def conditional_modifier(context, action):
        if action["id"] == id:
            modifier(context, action)
    return conditional_modifier


def action_id_target(id, actuator):
    def match(context, action):
        return action["id"] == id
    return (match, actuator)


def go_back_action(context, action):
    game = context.game
    if game and game.location.parent:
        game.location = game.location.parent


stockholm = GameLocation(
    title="Stockholm",
    position=(0, 0),
    background="https://images.unsplash.com/photo-1508189860359-777d945909ef?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    actions=[]
)

stockholm_locations = [
    GameLocation(
        parent=stockholm,
        title="Kungliga Biblioteket",
        position=(0, 0)
    )
]

uppsala = GameLocation(
    title="Uppsala",
    background="https://images.unsplash.com/photo-1553106789-988f8d3c366f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
    position=(0, 0),
    actions=[]
)

uppsala_locations = [
    GameLocation(
        parent=uppsala,
        title="Carolina Rediviva",
        background="https://images.unsplash.com/photo-1596846751725-106e44410d51?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80",
        position=(0, 0),
    ),
    GameLocation(
        parent=uppsala,
        title="Ofvandahls hovkonditori",
        description=lorem_ipsum_data,
        background="https://images.unsplash.com/photo-1518892383208-347332432268?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
        title_image="https://images.unsplash.com/photo-1588956950505-3c8d99dac5d1?ixlib=rb-1.2.1&auto=format&fit=crop&w=658&q=80",
        position=(0, 0),
        actions=[
            GameAction(
                title="Have a fika",
                update=add_cash_modifier(-10)
            ),
            GameAction(
                title="Have a coffee",
                update=add_cash_modifier(-5)
            ),
            GameAction(
                title="Leave",
            )
        ],
        actuator=LocationVisit()
    ),
    GameLocation(
        parent=uppsala,
        title="Studentvägen",
        background="https://images.unsplash.com/photo-1560685145-bafda179f1b7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80",
        position=(0, 0)
    ),
    GameLocation(
        parent=uppsala,
        title="Polacksbacken",
        position=(0, 0),
        actuator=StaticActuator(
            {
                "type": "info",
                "title": "Polacksbacken",
                "markdown": lorem_ipsum_data,
                "titleImage": "https://images.unsplash.com/photo-1477238134895-98438ad85c30?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
                "background": "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
                "actions": [
                    {
                        "type": "navigate",
                        "title": "Study engineering",
                        "id": "engineering"
                    },
                    {
                        "type": "navigate",
                        "title": "Study math",
                        "id": "math"
                    },
                    {
                        "type": "navigate",
                        "title": "Study physics",
                        "id": "physics"
                    },
                    {
                        "type": "navigate",
                        "title": "Study computer science",
                        "id": "computer-science"
                    },
                    {
                        "type": "navigate",
                        "title": "Leave",
                        "id": "leave"
                    }
                ],
            },
            [
                go_back_action
            ],
            [
                action_id_target(
                    "engineering",
                    StaticActuator(
                        {
                            "type": "info",
                            "title": "Engineering",
                            "markdown": lorem_ipsum_data,
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
                ),
            ]
        )
    ),
    GameLocation(
        parent=uppsala,
        title="Flogsta",
        background="https://images.unsplash.com/photo-1567513022376-eaef86f2f92b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80",
        position=(0, 0)
    ),
]

cities = [
    uppsala,
    stockholm
]

world = StaticGameWorld(
    locations=(
        cities + stockholm_locations + uppsala_locations
    )
)
