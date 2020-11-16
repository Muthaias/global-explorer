from global_explorer import GameMap, GameLocation

stockholm = GameMap(
    title = "Stockholm",
    background = "https://images.unsplash.com/photo-1508189860359-777d945909ef?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    locations = [
        GameLocation(
            title = "Kungliga Biblioteket",
            position = (0, 0)
        )
    ]
)

uppsala = GameMap(
    title = "Uppsala",
    background = "https://images.unsplash.com/photo-1553106789-988f8d3c366f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
    locations = [
        GameLocation(
            title = "Carolina Rediviva",
            position = (0, 0)
        ),
        GameLocation(
            title = "Ramboo",
            position = (0, 0)
        ),
        GameLocation(
            title = "Stundentvägen",
            position = (0, 0)
        ),
        GameLocation(
            title = "Polacksbacken",
            position = (0, 0)
        ),
        GameLocation(
            title = "Flogsta",
            position = (0, 0)
        ),
        GameLocation(
            title = "Norrlands Nation",
            position = (0, 0)
        )
    ]
)

maps = [
    uppsala,
    stockholm
]