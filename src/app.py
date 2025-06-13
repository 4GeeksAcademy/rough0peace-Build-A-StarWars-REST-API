"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favorites 
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Person.query.all() 
    person_dictionaries = []
    for person in people: 
        person_dictionaries.append(
            person.serialize()
        )
    return jsonify(person_dictionaries), 200 

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person():
    pass

@app.route('/planets', methods=['GET'])
def get_all_planets():
    pass

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(): 
    pass

@app.route('/users', methods=['GET'])
def get_all_users():
    pass

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    pass

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet():
    pass

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person():
    pass

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet():
    pass

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person():
    pass





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
