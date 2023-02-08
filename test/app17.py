from flask import Flask, request, render_template
app = Flask(__name__)

accounts = {
    "client1": {"balance": 1000},
    "client2": {"balance": 2000},
    "client3": {"balance": 3000}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deposit", methods=["POST"])
def deposit():
    client = request.form["client"]
    amount = int(request.form["amount"])
    accounts[client]["balance"] += amount
    return render_template("index.html", message=f"Deposited {amount} to {client}'s account.")

@app.route("/withdraw", methods=["POST"])
def withdraw():
    client = request.form["client"]
    amount = int(request.form["amount"])
    if accounts[client]["balance"] >= amount:
        accounts[client]["balance"] -= amount
        return render_template("index.html", message=f"Withdrew {amount} from {client}'s account.")
    else:
        return render_template("index.html", message=f"Not enough balance in {client}'s account.")

if __name__ == '__main__':
    app.run()
