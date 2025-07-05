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

@app.route('/person', methods=['GET'])
def get_all_people():
    people = Person.query.all() 
    return jsonify([person.serialize() for person in people]), 200 

@app.route('/person/<int:person_id>', methods=['GET'])
def get_one_person(person_id):  
    person = Person.query.get(person_id)  
    if person is None:
        return jsonify({"message": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200  

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):  
    planet = Planet.query.get(planet_id)  
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200  

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400
        
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200  

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):  

    # check user_id to see if it is in the request
    data = request.get_json()
    if data is None or 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    # Check if user exists in the database 
    user = User.query.get(data['user_id'])
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    # Check if planet exists
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    # Check if favorite already exists
    existing_favorite = Favorites.query.filter_by(
        user_id=data['user_id'], 
        planet_id=planet_id
    ).first()
    if existing_favorite is not None:
        return jsonify({"error": "Favorite already exists"}), 400
    
    # Create new favorite
    new_favorite = Favorites(
        user_id=data['user_id'],
        planet_id=planet_id
    )

    try:
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201  
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/person/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):  
    data = request.get_json()
    if data is None or 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    person = Person.query.get(person_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    
    user = User.query.get(data['user_id'])
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    existing_favorite = Favorites.query.filter_by(
        user_id=data['user_id'],
        person_id=person_id
    ).first()
    if existing_favorite is not None:
        return jsonify({"error": "Favorite already exists"}), 400
    
    new_favorite = Favorites(
        user_id=data['user_id'],
        person_id=person_id  
    )

    try:
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201  
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):  
    data = request.get_json()
    if data is None or 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    existing_favorite = Favorites.query.filter_by(
        user_id=data['user_id'],
        planet_id=planet_id
    ).first()
    
    if existing_favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    
    try:
        db.session.delete(existing_favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/person/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):  
    data = request.get_json()
    if data is None or 'user_id' not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    existing_favorite = Favorites.query.filter_by(
        user_id=data['user_id'],
        person_id=person_id
    ).first()
    
    if existing_favorite is None:
        return jsonify({"error": "Favorite not found"}), 404
    
    try:
        db.session.delete(existing_favorite)
        db.session.commit()
        return jsonify({"message": "Favorite person deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)