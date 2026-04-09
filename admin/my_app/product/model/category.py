from my_app import db

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, HiddenField, FormField, FieldList
from wtforms.validators import InputRequired, ValidationError


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

def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError("La categoría: %s ya fue tomada" % field.data)

def check_category(contain=True):
    def _check_category(form, field):
        print(form.id.data)
        if contain:
            res = Category.query.filter(Category.name.like("%"+field.data+"%")).first()
        else:
            res = Category.query.filter(Category.name.like(field.data)).first()

        if res and form.id.data and res.id != int(form.id.data):
            raise ValidationError("La categoría: %s ya fue tomada" % field.data)
    return _check_category

class PhoneForm(FlaskForm):
    phoneCode = StringField("Código teléfono")
    countryCode = StringField("Código país")
    phone = StringField("Teléfono")

class PhoneForm2(FlaskForm):
    phoneCode2 = StringField("Código teléfono2")

class CategoryForm(PhoneForm):#, PhoneForm2
    name = StringField('Nombre', validators=[InputRequired(), check_category(contain=False)])
    id = HiddenField('Id')
    recaptcha = RecaptchaField()
    #phonelist = FormField(PhoneForm)
    #phones = FieldList(FormField(PhoneForm))

