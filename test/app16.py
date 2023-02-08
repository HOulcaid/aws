from flask import Flask, request

app = Flask(__name__)

clients = {
    "client1": {"balance": 1000},
    "client2": {"balance": 200},
    "client3": {"balance": 300},
    "client4": {"balance": 4000},
    "client5": {"balance": 5000},
    "client6": {"balance": 6000},
}

@app.route('/clients/<string:client_id>', methods=['GET'])
def get_balance(client_id):
    if client_id in clients:
        return {"balance": clients[client_id]["balance"]}
    else:
        return {"error": "Client not found"}, 404

@app.route('/clients/<string:client_id>/deposit', methods=['POST'])
def deposit(client_id):
    if client_id in clients:
        amount = request.json.get("amount")
        if amount:
            clients[client_id]["balance"] += amount
            return {"balance": clients[client_id]["balance"]}
        else:
            return {"error": "Missing 'amount' parameter"}, 400
    else:
        return {"error": "Client not found"}, 404

@app.route('/clients/<string:client_id>/withdraw', methods=['POST'])
def withdraw(client_id):
    if client_id in clients:
        amount = request.json.get("amount")
        if amount:
            if clients[client_id]["balance"] >= amount:
                clients[client_id]["balance"] -= amount
                return {"balance": clients[client_id]["balance"]}
            else:
                return {"error": "Insufficient balance"}, 400
        else:
            return {"error": "Missing 'amount' parameter"}, 400
    else:
        return {"error": "Client not found"}, 404

if __name__ == '__main__':
    app.run()
