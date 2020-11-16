
import webview
from uuid import uuid4

class Account:
    def __init__(self, transactions, owner = "Anonymous", card_number = "1111 1111 1111 1111", card_valid_thru = "12/20"):
        self.transactions = transactions
        self.balance = self.calculate_balance()
        self.owner = owner
        self.card_number = card_number
    
    def calculate_balance(self):
        balance = 0
        for transaction in transactions:
            balance = balance + transaction.amount
        return balance
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.balance = balance + transaction.amount

class Skills:
    def __init__(self, description, skill_points):
        self.description = description
        self.skill_points = skill_points

class Player:
    def __init__(self, account, skills, name = None):
        self.id = str(uuid4())
        self.account = account
        self.skills = skills
        self.name = name if name != None else account.owner
        self.skill_points = self.calculate_skill_points()
    
    def calculate_skill_points(self):
        return {
            "skill_id": 1337
        }
    
    def add_skill(self, skill):
        self.skills.append(skill)
        self.skill_points = self.skill_points

    def content():
        return {
            "id": self.id,
            "account": {
                "card_number": self.account.card_number,
                "balance": self.account.balance,
                "valid_thru": self.account.card_valid_thru
            }
        }


class Menu:
    def __init__(self, entries, background, exit_actuator = None):
        self.entries = entries
        self.background = background
        self.exit_actuator = exit_actuator
    
    def content(self):
        return {
            "type": "menu",
            "background": self.background,
            "actions": self.actions(),
            "backAction": {
                "type": "exit"
            } if self.exit_actuator else None
        }

    def actions(self):
        return [
            {
                "type": "navigate",
                "title": entry.title,
                "id": entry.id
            }
            for entry in self.entries
        ]

    def action(self, action):
        if action["type"] == "navigate":
            entry = next((e for e in self.entries if e.id == action["id"]), None)
            if entry:
                actuator = entry.actuator
                if hasattr(actuator, "exit_actuator"):
                    actuator.exit_actuator = self
                return actuator
        elif action["type"] == "exit" and self.exit_actuator != None:
            return self.exit_actuator 

class MenuEntry:
    def __init__(self, type, actuator, title, id = None):
        self.type = type
        self.id = id if id != None else str(uuid4())
        self.title = title
        self.actuator = actuator

class StaticActator:
    def __init__(self, content):
        self.__content = content
    
    def content(self):
        return self.__content

class GlobalExplorerView:
    def __init__(self, actuator):
        self.actuators = [actuator]

    def version(self):
        return "0.0.1"

    def content(self):
        actuator = self.actuator()

        print("content", actuator)
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
                print(selectedActuator)
                print("Actuator: " + str(existingActuatorIndex))
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