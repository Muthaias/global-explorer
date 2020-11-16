from global_explorer import GameMap, GameLocation, StaticActuator, Transaction


def add_cash_modifier(amount):
    def modifier(parent):
        if hasattr(parent, "player"):
            parent.player.account.add_transaction(Transaction(amount))
    return modifier


stockholm = GameMap(
    title="Stockholm",
    background="https://images.unsplash.com/photo-1508189860359-777d945909ef?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    locations=[
        GameLocation(
            title="Kungliga Biblioteket",
            position=(0, 0)
        )
    ]
)

uppsala = GameMap(
    title="Uppsala",
    background="https://images.unsplash.com/photo-1553106789-988f8d3c366f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
    locations=[
        GameLocation(
            title="Carolina Rediviva",
            position=(0, 0)
        ),
        GameLocation(
            title="Ofvandahls hovkonditori",
            position=(0, 0),
            actuator=StaticActuator({
                "type": "info",
                "title": "Ofvandahls hovkonditori",
                "markdown": "Ofvandahls är ett anrikt kafé och konditori i korsningen av S:t Olofsgatan (tidigare Järnbrogatan) och Sysslomansgatan i Uppsala. Etablissemanget, som under lång tid också var hovkonditori, grundades under namnet Café Dahlia år 1878 av Erik Ofvandahl. Ofvandahl var känd även som pekoralist och utgivare av en rad diktsamlingar som nöjeslästes av Uppsalastudenterna.[1] Ofvandahlhuset är kulturminnesmärkt. Rörelsen drevs från 1949 till 1971 av Erik Ofvandahls döttrar, Ragnhild och Anna.",
                "titleImage": "https://images.unsplash.com/photo-1588956950505-3c8d99dac5d1?ixlib=rb-1.2.1&auto=format&fit=crop&w=658&q=80",
                "background": "https://images.unsplash.com/photo-1518892383208-347332432268?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80",
                "finishAction": {
                    "type": "navigate",
                    "title": "Finish",
                    "id": "finish"
                },
            }, add_cash_modifier(-100))
        ),
        GameLocation(
            title="Studentvägen",
            position=(0, 0)
        ),
        GameLocation(
            title="Polacksbacken",
            position=(0, 0)
        ),
        GameLocation(
            title="Flogsta",
            position=(0, 0)
        ),
        GameLocation(
            title="Norrlands Nation",
            position=(0, 0)
        )
    ]
)

maps = [
    uppsala,
    stockholm
]
