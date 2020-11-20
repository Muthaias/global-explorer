from uuid import uuid4
import random


class TrotterState:
    def __init__(
        self,
        player,
        trace=None,
        time=None,
    ):
        self.__player = player
        self.__time = time if time is not None else 0
        self.__trace = trace if trace is not None else []

    @property
    def time(self):
        return self.__time

    @property
    def trace(self):
        return iter(self.__trace)

    @property
    def player(self):
        return self.__player

    def pass_time(self, seconds=0):
        self.__time += seconds

    def add_trace(self, node):
        self.__trace.append(node)


class Player:
    def __init__(self, account, skills, name=None):
        self.id = str(uuid4())
        self.account = account
        self.skills = skills
        self.name = name if name is not None else account.owner
        self.skill_points = self.calculate_skill_points()

    def calculate_skill_points(self):
        return {
            "skill_id": 1337
        }

    def add_skill(self, skill):
        self.skills.append(skill)
        self.skill_points = self.skill_points

    def content(self):
        return {
            "id": self.id,
            "name": self.name,
            "account": {
                "card_number": self.account.card_number,
                "balance": self.account.balance,
                "valid_thru": self.account.card_valid_thru
            }
        }


class Account:
    def __init__(
        self,
        transactions=[],
        owner="Anonymous",
        card_number=None,
        card_valid_thru="12/20"
    ):
        self.transactions = transactions
        self.balance = self.calculate_balance()
        self.owner = owner
        self.card_number = self.random_card_number()
        self.card_valid_thru = card_valid_thru

    def random_card_number(self):
        card_elements = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        card_number = ""
        for i in range(0, 16):
            card_number += random.choice(card_elements)
            card_number += " " if i % 4 == 3 else ""
        return card_number

    def calculate_balance(self):
        balance = 0
        for transaction in self.transactions:
            balance += transaction.amount
        return balance

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.balance += transaction.amount
        pass


class Transaction:
    def __init__(self, amount, description=None):
        self.amount = amount
        self.description = description


class Skills:
    def __init__(self, description, skill_points):
        self.description = description
        self.skill_points = skill_points
