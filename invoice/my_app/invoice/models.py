from my_app import db

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class Sell(db.Model):
    __tablename__= 'sells'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    company = db.Column(db.String(255))
    sellproducts = db.relationship('SellProduct')

class SellProduct(db.Model):
    __tablename__= 'sell_products'
    id = db.Column(db.Integer, primary_key=True)  
    sell_id = db.Column(db.Integer, db.ForeignKey('sells.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product')

class InvoiceForm(FlaskForm):
    name = StringField("Nombre", validators=[InputRequired()])
    surname = StringField("Apellido", validators=[InputRequired()])
    company = StringField("Empresa", validators=[InputRequired()])