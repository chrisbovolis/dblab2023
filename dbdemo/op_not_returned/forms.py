from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField,SelectMultipleField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class SearchForm(FlaskForm):
    
    first_name = StringField(label = "User's first name")

    last_name = StringField(label = "User's last name")

    delay = StringField(label = "Delay")

    submit = SubmitField("Create")

class UserForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    status = StringField(label = "Status", validators = [DataRequired(message = "Status is a required field.")])
    
    punctual = StringField(label = "Punctual", validators = [DataRequired(message = "Punctuality is a required field.")])

    submit = SubmitField("Create")