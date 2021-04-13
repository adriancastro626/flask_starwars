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
from models import db, User, Character, Planet
import json

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#from models import Person

app = Flask(__name__)


app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_APP_KEY')  # Change this!

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/login", methods=["POST"])
def login_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })




###############################################################
@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
   
    return jsonify(User.getAllusers()), 200

@app.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def get_Oneuser(id): 
    current_user_id = get_jwt_identity()
    user = User.filter.get(current_user_id)
    return jsonify(User.getUser(id)), 200    

@app.route('/user', methods=['POST'])
def new_user():
    request_body_user=request.data
    decoded_object = json.loads(request_body_user)
    return jsonify(User.create_user(decoded_object)), 200

@app.route('/user/<int:id>/newChar/<int:char_id>', methods=['PUT'])
def new_favChar(id, char_id):
    return jsonify(User.newFavChar(id, char_id))

@app.route('/user/<int:id>/newPlanet/<int:planet_id>', methods=['PUT'])
def new_favPlanet(id, planet_id):
    return jsonify(User.newFavPlanet(id, planet_id))

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    return jsonify(User.deleteUser(id)), 200

#########################################################
@app.route('/character', methods=['GET'])
def get_character():
    return jsonify(Character.getAllcharacters()), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_OneChar(id):
    return jsonify(Character.getChar(id)), 200  

# @app.route('/character', methods=['POST'])
# def new_character():
#     request_body_char=request.data
#     decoded_object = json.loads(request_body_char)
#     return jsonify(Character.create_character(decoded_object)), 200

###########################################################
@app.route('/planet', methods=['GET'])
def get_planet():
    return jsonify(Planet.getAllplanets()), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_OnePlanet(id):
    return jsonify(Planet.getPlanet(id)), 200  

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
