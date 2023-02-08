from datetime import datetime
from flask import Flask, request, jsonify

class BankAccount:
    def __init__(self):
        self.transactions = []

    def deposit(self, amount):
        self.transactions.append((datetime.now(), amount, self.balance + amount))
        self.balance += amount

    def withdrawal(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.transactions.append((datetime.now(), -amount, self.balance - amount))
        self.balance -= amount

    def statement(self):
        return self.transactions


app = Flask(__name__)

@app.route("/deposit", methods=["POST"])
def deposit():
    amount = request.json["amount"]
    account.deposit(amount)
    return jsonify(success=True)

@app.route("/withdrawal", methods=["POST"])
def withdrawal():
    amount = request.json["amount"]
    try:
        account.withdrawal(amount)
    except ValueError as e:
        return jsonify(success=False, message=str(e))
    return jsonify(success=True)

@app.route("/statement", methods=["GET"])
def statement():
    return jsonify(account.statement())

if __name__ == "__main__":
    account = BankAccount()
    app.run()
