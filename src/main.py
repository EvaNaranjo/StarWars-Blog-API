"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favourite
#from models import P

api = Blueprint("api", __name__)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/person', methods=['GET'])
def get_all_person():
    persons = Person.query.all()
    list_all_person = list(map(lambda person: person.serialize(),persons))
    return jsonify(list_all_person),200

@app.route("/person/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person=Person.query.get(person_id)

    if person==None:
        resp = "This person does not exist"
    else:
        resp =person.serialize()
    
    return jsonify(resp),200

@app.route('/planet', methods=['GET'])
def get_planets_all():
    planets = Planet.query.all()
    list_all_planet = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(list_all_planet),200

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet=Planet.query.get(planet_id)

    if planet==None:
        resp = "This planet does not exist"
    else:
        resp =planet.serialize()
    
    return jsonify(resp),200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user=User.query.get(user_id)
    if user==None:
        resp = "User does not exist"
    else:
        resp = user.serialize()

    return jsonify(resp),200
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
