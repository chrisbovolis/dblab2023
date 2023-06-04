from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

def validate_password_length(form, field):
    if len(field.data) < 10:
        raise ValidationError('Password must be at least 10 characters long.')

class PasswordForm(FlaskForm):
    
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field."), validate_password_length])

    submit = SubmitField("Create")