from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

class LendingForm(FlaskForm):
    starting_date = StringField(label = "Starting date")

    due_date = StringField(label = "Due date")

    userid = StringField(label="User's name", validators=[DataRequired(message="User's name is a required field.")])

    relid = StringField(label = "Book's name", validators = [DataRequired(message = "Book's name is a required field.")])

    return_date = StringField(label = "Return date")

    returned = StringField(label = "Returned?")

    submit = SubmitField("Create")

class InsertLendingForm(FlaskForm):
    due_date = StringField(label = "Due date")

    userid = StringField(label="User's id", validators=[DataRequired(message="User's name is a required field.")])

    relid = StringField(label = "Book's id", validators = [DataRequired(message = "Book's name is a required field.")])

    submit = SubmitField("Create")