from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

class ReservationForm(FlaskForm):
    start_date = StringField(label = "Starting date")

    due_date = StringField(label = "Due date")

    reservation_date = StringField(label = "Reservation date")

    userid = StringField(label="User's name", validators=[DataRequired(message="User's name is a required field.")])

    relid = StringField(label = "Book's name", validators = [DataRequired(message = "Book's name is a required field.")])

    active = StringField(label = "Active?")

    submit = SubmitField("Create")

class InsertReservationForm(FlaskForm):
    userid = StringField(label="User's id", validators=[DataRequired(message="User's name is a required field.")])

    relid = StringField(label = "Book's id", validators = [DataRequired(message = "Book's name is a required field.")])

    submit = SubmitField("Create")