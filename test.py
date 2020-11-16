
import webview
from global_explorer import Menu, MenuEntry, StaticActator

class GlobalExplorerView:
    def __init__(self, actuator):
        self.actuators = [actuator]

    def version(self):
        return "0.0.1"

    def content(self):
        actuator = self.actuator()
        try:
            return actuator.content()
        except Exception as e:
            print("Get content failed")
            print(e)
    
    def player(self):
        actuator = self.actuator()
        if hasattr(actuator, "player"):
            return player.content()
        return None


    def actuator(self):
        return self.actuators[-1]

    def action(self, action):
        actuator = self.actuator()
        try:
            selectedActuator = actuator.action(action)
            
            if selectedActuator:
                existingActuatorIndex = next((i for i, e in enumerate(self.actuators) if actuator is selectedActuator), None)
                if existingActuatorIndex is None:
                    self.actuators.append(selectedActuator)
                else:
                    self.actuators = self.actuators[0:existingActuatorIndex]
        except Exception as e:
            print(e)

noop = StaticActator({
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

new_game_menu = Menu(
    [
        MenuEntry(
            type = "navigate",
            title = "Stockholm",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Uppsala",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Göteborg",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Malmö",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Kiruna",
            actuator = noop
        )
    ],
    "https://images.unsplash.com/photo-1554123168-b400f9c806ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
    noop
)

main_menu = Menu(
    [
        MenuEntry(
            type = "navigate",
            title = "New game",
            actuator = new_game_menu
        ),
        MenuEntry(
            type = "navigate",
            title = "Load game",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Settings",
            actuator = noop
        ),
        MenuEntry(
            type = "navigate",
            title = "Credits",
            actuator = noop
        ),
    ],
    "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80"
)
print(main_menu.content())
api = GlobalExplorerView(main_menu)
webview.create_window("Global Explorer", "assets/index.html", js_api=api)
webview.start()