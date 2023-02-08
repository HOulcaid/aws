from flask import Flask, request
app = Flask(__name__)

employees = [
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



@app.route('/', methods=['GET'])
def home():
 return '''<h1>AWS Course API</h1>
<p>Sup deVinci.</p>'''


@app.route('/employees', methods=['GET'])
def get_employees():
    return {'employees': employees}

@app.route('/employees', methods=['POST'])
def add_employee():
    employee = {
        'id': employees[-1]['id'] + 1,
        'name': request.json['name']
    }
    employees.append(employee)
    return {'employee': employee}

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    for employee in employees:
        if employee['id'] == employee_id:
            employees.remove(employee)
            return {'message': 'Employee has been deleted'}

if __name__ == '__main__':
    app.run(debug=True)