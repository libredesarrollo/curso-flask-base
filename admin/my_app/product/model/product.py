from my_app import db

from decimal import Decimal

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, NumberRange

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    #file = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
        nullable=False)
    #category = db.relationship('Category', backref='products',lazy=True)

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
        #self.file = file

    def __repr__(self):
        return '<Product %r>' % (self.name)

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    category_id = SelectField('Categoría', coerce=int)
    file = FileField('Archivo') #, validators=[FileRequired()]
    