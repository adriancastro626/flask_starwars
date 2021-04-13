from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, url_for

db = SQLAlchemy()

fav_char = db.Table('fav_chars', db.metadata, 
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")), 
    db.Column("char_id", db.Integer, db.ForeignKey("characters.id")))

fav_planet = db.Table('fav_planets', db.metadata, 
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")), 
    db.Column("plan_id", db.Integer, db.ForeignKey("planets.id")))

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    username=db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    characters = db.relationship("Character", secondary=fav_char, back_populates="users") 
    planets = db.relationship("Planet", secondary=fav_planet, back_populates="users") 
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username":self.username,
            "characters": list(map(lambda x: x.serialize(), self.characters)),
            "planets": list(map(lambda x: x.serialize(), self.planets))
            # do not serialize the password, its a security breach
        }
    
    def getAllusers():
        users_query = User.query.all()
        all_users = list(map(lambda x: x.serialize(), users_query))
        return(all_users)
    
    def getUser(id):
        user_query = User.query.get(id)
        return(user_query.serialize())


    def create_user(request_body_user):
        user = User(name=request_body_user["name"], lastname=request_body_user["lastname"], username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
        db.session.add(user)
        db.session.commit()
        return("An user has been added")

    def deleteUser(id):
        user = User.query.get(id)
        if user is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user)
        db.session.commit()
        return("The user has been deleted")

    def newFavChar(id, char_id):
        user = User.query.get(id)
        char = Character.query.get(char_id) 
        if user is None:
            raise APIException('User not found', status_code=404)
        if char is None:
            raise APIException('Character not found', status_code=404)
       
        user.characters.append(char)
        db.session.commit()
        return user.serialize()
    
    def newFavPlanet(id, planet_id):
        user = User.query.get(id)
        planet = Planet.query.get(planet_id) 
        if user is None:
            raise APIException('User not found', status_code=404)
        if planet is None:
            raise APIException('Planet not found', status_code=404)
       
        user.planets.append(planet)
        db.session.commit()
        return user.serialize()


class Character(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender=db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    hair_color=db.Column(db.String(250), nullable=False)
    eye_color=db.Column(db.String(250), nullable=False)
    
    
    users = db.relationship("User", secondary=fav_char, back_populates="characters") 
   
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
            # do not serialize the password, its a security breach
        }
    
    def getAllcharacters():
        characters_query = Character.query.all()
        all_characters = list(map(lambda x: x.serialize(), characters_query))
        return(all_characters)
    
    def getChar(id):
        char_query = Character.query.get(id)
        return(char_query.serialize())

    # def create_character(request_body_char):
    #     char1 = Character(name=request_body_char["name"], birth_year=request_body_char["birth_year"], gender=request_body_char["gender"], height=request_body_char["height"], eye_color=request_body_char["eye_color"], hair_color=request_body_char["hair_color"])
    #     db.session.add(char1)
    #     db.session.commit()
    #     return("A character has been added")

class Planet(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)

    users = db.relationship("User", secondary=fav_planet, back_populates="planets") 
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate":self.climate,
            "population":self.population,
            "orbital_period":self.orbital_period,
            "rotation_period":self.rotation_period,
            "diameter":self.diameter  
            
            # do not serialize the password, its a security breach
        }
    
    def getAllplanets():
        planets_query = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), planets_query))
        return(all_planets)

    def getPlanet(id):
        planet_query = Planet.query.get(id)
        return(planet_query.serialize())

    # def create_planet(request_body_planet):
    #     planet = Planet(name=request_body_planet["name"], population=request_body_planet["population"], gender=request_body_char["gender"], height=request_body_char["height"], eye_color=request_body_char["eye_color"], hair_color=request_body_char["hair_color"])
    #     db.session.add(planet)
    #     db.session.commit()
    #     return("A planet has been added")
    
    