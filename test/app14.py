from flask import Flask, request

app = Flask(__name__)

clients = {
    "client1": {"balance": 1000},
    "client2": {"balance": 2000},
    "client3": {"balance": 3000},
    "client4": {"balance": 4000},
}

@app.route('/deposit', methods=['POST'])
def deposit():
    client_id = request.form.get('client_id')
    amount = int(request.form.get('amount'))

    if client_id in clients:
        clients[client_id]["balance"] += amount
        return "Deposit successful! New balance: {}".format(clients[client_id]["balance"])
    else:
        return "Client not found.", 404

@app.route('/withdraw', methods=['POST'])
def withdraw():
    client_id = request.form.get('client_id')
    amount = int(request.form.get('amount'))

    if client_id in clients:
        if clients[client_id]["balance"] >= amount:
            clients[client_id]["balance"] -= amount
            return "Withdrawal successful! New balance: {}".format(clients[client_id]["balance"])
        else:
            return "Insufficient balance.", 400
    else:
        return "Client not found.", 404

@app.route('/balance', methods=['GET'])
def balance():
    client_id = request.args.get('client_id')

    if client_id in clients:
        return "Current balance: {}".format(clients[client_id]["balance"])
    else:
        return "Client not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
