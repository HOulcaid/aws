from flask import Flask, render_template, request, redirect, url_for

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
    return redirect(url_for("display_balance"))

@app.route("/balance")
def display_balance():
    return render_template("index.html", balance=account.display_balance(), transactions=account.display_transactions())

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        deposit_amount = int(request.form["deposit_amount"])
        account.deposit(deposit_amount)
        return redirect(url_for("display_balance"))
    return render_template("deposit.html")

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        withdrawal_amount = int(request.form["withdrawal_amount"])
        account.withdraw(withdrawal_amount)
        return redirect(url_for("display_balance"))
    return render_template("withdraw.html")

if __name__ == "__main__":
    app.run()
