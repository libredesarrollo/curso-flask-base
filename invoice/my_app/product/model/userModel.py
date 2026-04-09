

from flask_user.forms import RegisterForm,ChangeUsernameForm

from wtforms.validators import DataRequired
from wtforms import ValidationError, validators
from wtforms import StringField

from my_app.auth.model.user import User


class CustomRegisterForm(RegisterForm):
    # Add a country field to the Register form
    country = StringField('Country', validators=[DataRequired()])

class CustomChangeUsernameForm(ChangeUsernameForm):

    new_username = StringField('New Username', validators=[
        validators.DataRequired('Username is required'),
    ])

    def validate_new_username(form, field):

        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('This Username is already in use. Please try another one.')