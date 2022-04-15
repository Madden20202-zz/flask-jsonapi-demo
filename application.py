from flask import Flask
from falsk_sqlalchemy import SQLAlchemy

# Create a new Flask app
app = Flask(__name__)

# Set up the SQLAlchemy
app.config['SQLACHEMY_DATABASE_URL'] = 'sqlite:////artists.db'
db = SQLAlchemy(app)

# Define a class for the Artist Table
class Artist(db.Model):
    id = db.Column(db.Integer, prinary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    genre = db.Column(db.String)

# Create a table
db.create_all()