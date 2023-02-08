from flask import Flask, request, jsonify

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
