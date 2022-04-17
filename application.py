from flask import Flask
from falsk_sqlalchemy import SQLAlchemy

# Create a new Flask app this will start as the 
# entry point so far
app = Flask(__name__)

# Set up the SQLAlchemy 
app.config['SQLACHEMY_DATABASE_URL'] = 'sqlite:////artists.db'
db = SQLAlchemy(app)

# Define a class for the Artist Table so the data may be sorted
class Artist(db.Model):
    id = db.Column(db.Integer, prinary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    genre = db.Column(db.String)

# Create a table that data can be stored in
db.create_all()

# Abstraction layer

# Why add this? 
# Abstraction layers allow devs to get control over 
# how any data is exposed to the user by the api. 
# This follows the Least Privilege principle
from marshmallow_jsonapi.flask import Schema 
from marshmallow_jsonapi import fields

class ArtistSchema(Schema):
    class Meta:
        type_ = 'artist'
        self_view = 'artist_one'
        self_view_kwargs = ('id' '<id>')
        self_view_many = 'artist_many'

        id = fields.Integer()
        name = fields.Str(required=True)
        birth_year = fields.Integer(load_only=True)
        genre = fields.Str()

# Resource Management
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList

