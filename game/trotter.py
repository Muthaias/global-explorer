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

    def to_data(self, node_manager):
        id_trace = [node_manager.id_by_node(node) for node in self.__trace]
        player_data = self.__player.to_data()
        return {
            "trace": id_trace,
            "player": player_data,
            "time": self.__time,
        }

    @staticmethod
    def from_data(data, node_manager):
        player = Player.from_data(data["player"])
        time = data["time"]
        id_trace = data["trace"]
        trace = [node_manager.node_by_id(id) for id in id_trace]
        return TrotterState(
            player=player,
            trace=trace,
            time=time
        )


class Player:
    def __init__(self, account, skills, name=None, id=None):
        self.id = id if id else str(uuid4())
        self.account = account
        self.skills = []
        self.name = name if name else account.owner
        self.__skill_points = {}
        for skill in skills:
            self.add_skill(skill)

    @property
    def skill_points(self):
        return self.__skill_points

    def add_skill(self, skill):
        self.skills.append(skill)
        for key, value in skill.skill_points.items():
            self.__skill_points[key] = self.__skill_points.get(key, 0) + value

    def verify_skill(self, skill_id, value):
        return self.__skill_points.get(skill_id, 0) >= value

    def content(self):
        return {
            "id": self.id,
            "name": self.name,
            "account": {
                "card_number": self.account.card_number,
                "balance": self.account.balance,
                "valid_thru": self.account.card_valid_thru,
                "card_issuer": self.account.card_issuer
            },
        }

    def to_data(self):
        skills_data = [skill.to_data() for skill in self.skills]
        account_data = self.account.to_data()
        return {
            "id": self.id,
            "account": account_data,
            "skills": skills_data,
            "name": self.name,
        }

    @staticmethod
    def from_data(data):
        id = data["id"]
        name = data["name"]
        account = Account.from_data(data["account"])
        skills_data = data["skills"]
        skills = [
            Skill.from_data(skill_data)
            for skill_data
            in skills_data
        ]
        return Player(
            id=id,
            name=name,
            account=account,
            skills=skills
        )


class Account:
    def __init__(
        self,
        transactions=[],
        owner="Anonymous",
        card_number=None,
        card_valid_thru="12/20",
        card_issuer=None
    ):
        self.transactions = transactions
        self.balance = self.calculate_balance()
        self.owner = owner
        self.card_number = (
            self.random_card_number()
            if card_number is None
            else card_number
        )
        self.card_valid_thru = card_valid_thru
        self.card_issuer = (
            self.random_card_issuer()
            if card_issuer is None
            else card_issuer
        )

    def random_card_issuer(self):
        issuers = [
            "SHOWYA",
            "PRES",
            "Adeptcard",
            "Acecard",
            "Skilledcard",
        ]
        return random.choice(issuers)

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

    def to_data(self):
        transactions_data = [
            transaction.to_data()
            for transaction in self.transactions
        ]
        return {
            "transactions": transactions_data,
            "owner": self.owner,
            "card_number": self.card_number,
            "card_valid_thru": self.card_valid_thru,
            "card_issuer": self.card_issuer,
        }

    @staticmethod
    def from_data(data):
        transactions_data = data["transactions"]
        transactions = [
            Transaction.from_data(trans_data)
            for trans_data
            in transactions_data
        ]
        return Account(
            transactions=transactions,
            owner=data["owner"],
            card_number=data["card_number"],
            card_valid_thru=data["card_valid_thru"],
            card_issuer=data["card_issuer"]
        )


class Transaction:
    def __init__(self, amount, description=None):
        self.amount = amount
        self.description = description

    def to_data(self):
        return [self.amount, self.description]

    @staticmethod
    def from_data(data):
        [amount, description] = data
        return Transaction(
            amount=amount,
            description=description
        )


class Skill:
    def __init__(self, description, skill_points):
        self.description = description
        self.skill_points = skill_points

    def to_data(self):
        return [self.skill_points, self.description]

    @staticmethod
    def from_data(data):
        [skill_points, description] = data
        return Skill(
            skill_points=skill_points,
            description=description
        )
