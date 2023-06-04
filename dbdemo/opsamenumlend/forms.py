from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class LendingsbyschoolForm(FlaskForm):
    year = StringField(label = "Year", validators = [DataRequired(message = "Year is a required field.")])

    submit = SubmitField("Create")