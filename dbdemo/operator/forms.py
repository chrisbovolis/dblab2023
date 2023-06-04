from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

def validate_password_length(form, field):
    if len(field.data) < 10:
        raise ValidationError('Password must be at least 10 characters long.')
    
class OperatorForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])
 
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field."), validate_password_length])
    
    schoolid = StringField(label = "Schoolid", validators = [DataRequired(message = "Schoolid is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    submit = SubmitField("Create")