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
        artworks = Relationship(self_view = 'artist_artworks',
            self_view_kwargs = {'id': '<id>'},
            related_view = 'artwork_many',
            many = True,
            schema = 'ArtworkSchema',
            type_ = 'artwork')

class ArtworkSchema(Schema):
    class Meta:
        type_ = 'artwork'
        self_view = 'artwork_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'artwork_many'

    id = fields.Integer()
    title = fields.Str(required=True)
    artist_id = fields.Integer(required=True)
# Resource Management

# Each resource manager is a class that inherits from 
# the Flask-REST-JSONAPI classes under these notes

# Two attributes are taken, schema which tells the resource 
# layer what part of the abstraction level is to be used. Data_layer 
# indicates the session and data model to be used 

from flask_rest_jsonapi import Api, ResourceDetail, ResourceList

class ArtistMany(ResourceList):
    schema = ArtistSchema
    data_layer = {
        'session': db.session, 
        'model': Artist
        }

class ArtistOne(ResourceDetail):
    schema = ArtistSchema
    data_layer = {
        'session': db.session,
        'model': Artist
        }

# All routes need end points in order to 
# create a proper routing system 
# Three arguments are needed, the 
# data abstraction layer class, endpoint name, and the url path
api = Api(app)
api.route(ArtistMany, 'artist_many', '/artists')
api.route(ArtistOne, 'artist_one', '/artists/<int: id>')

# Main route for debug mode
if __name__ == '__main__':
    app.run(debug=True)

# What is a Relationship?
# Often, data in one table is related to 
# data within another. For example, an artist 
# with their artwork. The artist table is one the 
# artwork table is the other table. This is now
# able to be compared and brought together, so 
# data from both tables may be queried simultaneously

from marshmallow_jsonapi.flask import Relationship
from flask_rest_jsonapi import ResourceRelationship

# Define the Artwork Table
class Artwork(db.model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist_id = db.Column(db.Integer,
        db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', 
        backref=db.backref('artworks'))