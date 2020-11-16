from uuid import uuid4

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
    def __init__(self, transactions = [], owner = "Anonymous", card_number = "1337 1337 1337 1337", card_valid_thru = "12/20"):
        self.transactions = transactions
        self.balance = self.calculate_balance()
        self.owner = owner
        self.card_number = card_number
        self.card_valid_thru = card_valid_thru
    
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
    def __init__(self, amount, description = None):
        self.amount = amount
        self.description = description

class Skills:
    def __init__(self, description, skill_points):
        self.description = description
        self.skill_points = skill_points