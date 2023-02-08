from flask import Flask, request

app = Flask(__name__)

employees = [
    {
        "id": 1,
        "first_name": "Batman",
        "last_name": "Batman",
        "email": "batman@gmail.com"
    },
    {
        "id": 2,
        "first_name": "Superman",
        "last_name": "Superman",
        "email": "Superman@gmail.com"
    }
]

@app.route('/employees', methods=['GET'])
def get_employees():
    return {"employees": employees}

@app.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = [employee for employee in employees if employee['id'] == employee_id]
    return {"employee": employee[0]}

@app.route('/employee', methods=['POST'])
def add_employee():
    employee = {
        "id": request.json['id'],
        "first_name": request.json['first_name'],
        "last_name": request.json['last_name'],
        "email": request.json['email']
    }
    employees.append(employee)
    return {"employee": employee}

@app.route('/employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = [employee for employee in employees if employee['id'] == employee_id]
    employee[0]['first_name'] = request.json.get('first_name', employee[0]['first_name'])
    employee[0]['last_name'] = request.json.get('last_name', employee[0]['last_name'])
    employee[0]['email'] = request.json.get('email', employee[0]['email'])
    return {"employee": employee[0]}

@app.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = [employee for employee in employees if employee['id'] == employee_id]
    employees.remove(employee[0])
    return {"result": "Employee deleted"}

if __name__ == '__main__':
    app.run(debug=True)