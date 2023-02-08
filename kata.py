import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('bank.db')
    conn.execute(
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

    )
    return conn

@app.route('/clients', methods=['GET'])
def clients():
    conn = get_db()
    clients = conn.execute('''
        SELECT * FROM clients
    ''').fetchall()
    return jsonify(clients)

@app.route('/deposit', methods=['POST'])
def deposit():
    conn = get_db()
    client_id = request.form.get('client_id')
    amount = int(request.form.get('amount'))

    client = conn.execute('''
        SELECT * FROM clients WHERE id=?
    ''', (client_id,)).fetchone()
    if client:
        conn.execute('''
            UPDATE clients SET balance=balance+? WHERE id=?
        ''', (amount, client_id))
        conn.commit()
        return "Deposit successful! New balance: {}".format(client['balance'] + amount)
    else:
        return "Client not found.", 404

@app.route('/withdraw', methods=['POST'])
def withdraw():
    conn = get_db()
    client_id = request.form.get('client_id')
    amount = int(request.form.get('amount'))

    client = conn.execute('''
        SELECT * FROM clients WHERE id=?
    ''', (client_id,)).fetchone()
    if client:
        if client['balance'] >= amount:
            conn.execute('''
                UPDATE clients SET balance=balance-? WHERE id=?
            ''', (amount, client_id))
            conn.commit()
            return "Withdrawal successful! New balance: {}".format(client['balance'] - amount)
        else:
            return "Insufficient balance.", 400
    else:
        return "Client not found.", 404

@app.route('/balance', methods=['GET'])
def balance():
    conn = get_db()
    client_id = request.args.get('client_id')

    client = conn.execute('''
        SELECT * FROM clients WHERE id=?
    ''', (client_id,)).fetchone()
    if client:
        return "Current balance: {}".format(client['balance'])
    else:
        return "Client not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
