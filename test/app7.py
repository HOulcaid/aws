from flask import Flask, render_template, request

app = Flask(__name__)

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")

    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: {amount}")
        else:
            self.transactions.append(f"Insufficient funds for withdrawal: {amount}")

    def display_balance(self):
        return f"Balance: {self.balance}"

    def display_transactions(self):
        return "\n".join(self.transactions)

account = BankAccount(100)

@app.route("/")
def index():
    return render_template("index.html", balance=account.display_balance(), transactions=account.display_transactions())

@app.route("/deposit", methods=["POST"])
def deposit():
    deposit_amount = int(request.form["deposit_amount"])
    account.deposit(deposit_amount)
    return render_template("index.html", balance=account.display_balance(), transactions=account.display_transactions())

@app.route("/withdraw", methods=["POST"])
def withdraw():
    withdrawal_amount = int(request.form["withdrawal_amount"])
    account.withdraw(withdrawal_amount)
    return render_template("index.html", balance=account.display_balance(), transactions=account.display_transactions())

if __name__ == "__main__":
    app.run()
