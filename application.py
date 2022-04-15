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