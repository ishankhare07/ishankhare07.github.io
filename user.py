from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
import os
import hashlib
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
try:
    # running on heroku
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
except KeyError:
    # running on localhost
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@localhost'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    firstname       = db.Column(db.String, nullable=False)
    lastname        = db.Column(db.String, nullable=False)
    email           = db.Column(db.String, unique=True, nullable=False)
    password_hash   = db.Column(db.String, nullable=False)
    token           = db.Column(db.String)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hash = pwd_context.encrypt(password)

    def __repr__(self):
        return '<User %r>' %self.email

    def check_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        self.token = hashlib.sha512(os.urandom(24)).hexdigest()
        return self.token

    def jsonify(self):
        return json.dumps({
            "id": self.id,
            "email": self.email,
            })
