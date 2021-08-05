from my_app import db

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category',lazy=True)
    #products = db.relationship('Product',lazy='dynamic', backref=db.backref('category',lazy='select'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
