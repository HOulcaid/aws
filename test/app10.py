from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("clients.db")
    return conn

class BankAccount:
    def __init__(self, client_id, balance=0):
        self.client_id = client_id
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposit: {amount}")
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE clients SET balance = ? WHERE client_id = ?", (self.balance, self.client_id))
        conn.commit()
        conn.close()

    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: {amount}")
            conn = get_db()
            c = conn.cursor()
            c.execute("UPDATE clients SET balance = ? WHERE client_id = ?", (self.balance, self.client_id))
            conn.commit()
            conn.close()
        else:
            self.transactions.append(f"Insufficient funds for withdrawal: {amount}")

    def display_balance(self):
        return f"Balance: {self.balance}"

    def display_transactions(self):
        return "\n".join(self.transactions)

@app.route("/")
def index():
    return redirect(url_for("display_clients"))

@app.route("/clients", methods=["GET", "POST"])
def display_clients():
    if request.method == "POST":
        client_name = request.form["client_name"]
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO clients (client_name) VALUES (?)", (client_name,))
        conn.commit()
        conn.close()
        return redirect(url_for("display_clients"))
    conn = get_db()
    c = conn.cursor()
    clients = c.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return render_template("clients.html", clients=clients)

@app.route("/clients/<int:client_id>", methods=["GET", "DELETE"])
def client_detail(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "DELETE":
        c.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("display_clients"))
    conn.close()
    return render_template("client_detail.html", client=client)

@app.route("/clients/<int:client_id>/deposit", methods=["GET", "POST"])
def deposit(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "POST":
        amount = int(request.form["amount"])
        account = BankAccount(client_id, client[2])
        account.deposit(amount)
        return redirect(url_for("client_detail", client_id=client_id))
    conn.close()
    return render_template("deposit.html", client=client)

@app.route("/clients/<int:client_id>/withdraw", methods=["GET", "POST"])
def withdraw(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "POST":
        amount = int(request.form["amount"])
        account = BankAccount(client_id, client[2])
        account.withdraw(amount)
        return redirect(url_for("client_detail", client_id=client_id))
    conn.close()
    return render_template("withdraw.html", client=client)

if __name__ == "__main__":
    app.run()
