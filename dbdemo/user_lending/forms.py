from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

class UserLendingForm(FlaskForm):
    relid = IntegerField(label = "Book's ID", validators = [DataRequired(message = "Book's ID is a required field.")])

    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])
    
    starting_date = StringField(label = "Starting date")

    due_date = StringField(label = "Due date")

    return_date = StringField(label = "Return date")

    submit = SubmitField("Create")
