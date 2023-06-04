from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class SchoolForm(FlaskForm):
    schoolname = StringField(label = "School name", validators = [DataRequired(message = "School name is a required field.")])

    address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.")])

    city = StringField(label = "City", validators = [DataRequired(message = "City is a required field.")])
    
    tel = StringField(label = "Telephone number", validators = [DataRequired(message = "Telephone number is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    director = StringField(label = "Director", validators = [DataRequired(message = "Director is a required field.")])

    submit = SubmitField("Create")
