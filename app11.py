from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db():
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn

# table clients
clients = [
    {
        "id": 1,
        "first_name": "Bruce",
        "last_name": "Wayne",
        "email": "batman@gmail.com"
    },
    {
        "id": 2,
        "first_name": "Clark",
        "last_name": "Kent",
        "email": "Superman@gmail.com"
    },
    {
        "id": 3,
        "first_name": "Frank",
        "last_name": "Castle",
        "email": "Punisher@gmail.com"
    },
    {
        "id": 4,
        "first_name": "Tony",
        "last_name": "Stark",
        "email": "Ironman@gmail.com"
    }    
]


# Define a BankAccount class
class BankAccount:
    def __init__(self, client_id, balance):
        self.client_id = client_id
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE clients SET balance = ? WHERE client_id = ?", (self.balance, self.client_id))
        conn.commit()
        conn.close()
    
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE clients SET balance = ? WHERE client_id = ?", (self.balance, self.client_id))
        conn.commit()
        conn.close()
        return True

# Display a list of clients
@app.route("/")
def display_clients():
    conn = get_db()
    c = conn.cursor()
    clients = c.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return render_template("clients.html", clients=clients)

# Display details for a single client
@app.route("/clients/<int:client_id>", methods=["GET", "POST"])
def client_detail(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "POST":
        client_name = request.form["client_name"]
        initial_balance = int(request.form["initial_balance"])
        c.execute("""
            INSERT INTO clients (client_id, name, balance)
            VALUES (?, ?, ?)
        """, (client_id, client_name, initial_balance))
        conn.commit()

# Create a deposit endpoint
@app.route("/clients/<int:client_id>/deposit", methods=["GET", "POST"])
def deposit(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "POST":
        deposit_amount = int(request.form["deposit_amount"])
        account = BankAccount(client_id, client[2])
        account.deposit(deposit_amount)
        return redirect(url_for("display_clients"))
    return render_template("deposit.html", client=client)

# Create a withdraw endpoint
@app.route("/clients/<int:client_id>/withdraw", methods=["GET", "POST"])
def withdraw(client_id):
    conn = get_db()
    c = conn.cursor()
    client = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    if request.method == "POST":
        withdraw_amount = int(request.form["withdraw_amount"])
        account = BankAccount(client_id, client[2])
        if account.withdraw(withdraw_amount):
            return redirect(url_for("display_clients"))
        else:
            return render_template("error.html", client=client, message="Insufficient funds.")
    return render_template("withdraw.html", client=client)

# Create a delete endpoint
@app.route("/clients/<int:client_id>/delete", methods=["GET", "POST"])
def delete_client(client_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
    conn.commit()
    return redirect(url_for("display_clients"))

if __name__ == "__main__":
    app.run(debug=True)
