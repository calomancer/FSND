import os
from sqlalchemy import Column, String, Integer, Enum
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://ibgbpwczevccar:9ab97b4f9355e15b26da7c24ae1e63c0dff1041580229ce6a4012bcc5d649794@ec2-52-200-119-0.compute-1.amazonaws.com:5432/d4sl76ts7qk5r0'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

character_group = db.Table('character_group', db.metadata,
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
)

#Group Model includes Adventuring Team Name and DM of Team
class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    characters = db.relationship("Character", secondary=character_group, backref='groups')

    def full(self):
        return {
            "id": self.id,
            "name": self.name,
            "player_name": self.player_name,
        }
        
    def short(self):

        return {
            "id": self.id,
            "name": self.name,
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

#Player and Non Player Characters
class Character(db.Model):
    __tablename__ = 'character'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_name = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    race = db.Column(db.String)
    gender = db.Column(Enum('female','male', name="gender"), nullable=True) 
    job = db.Column(db.String)
    lvl = db.Column(db.Integer)
    currency = db.Column(db.Integer)

    def full(self):
        groups = self.groups
        if groups == []:
            g = None 
        else:
            g = groups[0].full()
        character = {
            "id": self.id,
            "player_name": self.player_name,
            "group": g,
            "name": self.name,
            "race": self.race,
            "gender": self.gender,
            "job": self.job,
            "lvl": self.lvl,
            "currency": self.currency
        }
        return character

    def short(self):
        character = {
            "id": self.id,
            "name": self.name,
            "job": self.job,
            "lvl": self.lvl,
        }
        return character
    
    def list(self):
        character = []
        character.append(self.id)
        character.append(self.name)
        character.append(self.race.capitalize())
        character.append(self.job.capitalize())
        character.append(self.gender.lower())
        character.append(self.lvl)
        character.append(self.currency)
        return character

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
