import flask
from flask import request, jsonify


app = flask.Flask(__name__)


#app.config["DEBUG"] = True

employees = [
   {'id': 0,
	'Nom': 'Ziyech',
	'‘Prénom’': 'Hakim',
	'email': 'HZiyech@frmf.ma',
   },
   {'id': 1,
	'Nom': 'Bounou',
	'Prénom': 'Yassine',
	'email': 'BYassine@frmf.ma',
   },
   {'id': 2,
	'Nom': 'Hakimi',
	'Prénom': 'Achraf',
	'email': 'HAchraf@frmf.ma',
	}
]


@app.route('/', methods=['GET'])
def home():
 return '''<h1>AWS Course API</h1>
<p>Sup deVinci.</p>'''

 
@app.route('/api/v1/resources/employees', methods=['GET'])
def api_id():

    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Erreur: Pas d’identifiant fourni. Veuillez spécifier un id."
 
    results = []
 

    for employee in employees:
        if employee['id'] == id:
            results.append(employee)

 
app.run()