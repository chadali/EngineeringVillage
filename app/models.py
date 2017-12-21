from app import db
from datetime import datetime, timedelta
import time

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(40), unique=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    google_image = db.Column(db.String())
    ev_points = db.Column(db.Integer)
 
    def __init__(self, email, first_name, last_name, image, points):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.google_image = image
        self.ev_points = points
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.email)
        
    def __self__(self):
        return '<User %r>' % (self.email)