
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
    def __init__(self, entries, background, exit_actuator):
        self.entries = entries
        self.background = background
        self.exit_actuator = exit_actuator
    
    def content(self):
        return {
            "type": "menu",
            "background": self.background,
            "actions": self.actions()
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
            [entry] = [entry for entry in self.entries if entry.id == action["id"]]
            if entry:
                return entry.actuator
        elif action["type"] == "exit":
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
            newActuator = actuator.action(action)
            if newActuator:
                self.actuators.append(newActuator)
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

main_menu = Menu(
    [
        MenuEntry(
            type = "navigate",
            title = "New game",
            actuator = noop
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
    "https://images.unsplash.com/photo-1503221043305-f7498f8b7888?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1935&q=80",
    noop
)
print(main_menu.content())
api = GlobalExplorerView(main_menu)
webview.create_window("Hello world", "assets/index.html", js_api=api)
webview.start()