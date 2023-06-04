from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError
    
class UserReviewForm(FlaskForm):
    text = StringField(label = "Review", validators = [DataRequired(message = "Review is a required field.")])

    bookid = StringField(label = "Book's id", validators = [DataRequired(message = "Book's id is a required field.")])
 
    
    scale = StringField(label = "Score", validators = [DataRequired(message = "Score is a required field.")])
    
    submit = SubmitField("Create")

class UserBookidForm(FlaskForm):
    
    bookid = StringField(label = "Book's id", validators = [DataRequired(message = "Book's id is a required field.")])
 
    submit = SubmitField("Create")

class UserReviewShowForm(FlaskForm):
    text = StringField(label = "Review", validators = [DataRequired(message = "Review is a required field.")])

    posting_date = StringField(label = "Upload Date", validators = [DataRequired(message = "Uploaddate is a required field.")])

    bookid = StringField(label = "Book's id", validators = [DataRequired(message = "Book's id is a required field.")])
 
    userid = StringField(label = "User's id", validators = [DataRequired(message = "User's id is a required field.")])
    
    scale = StringField(label = "Score", validators = [DataRequired(message = "Score is a required field.")])
    
    submit = SubmitField("Create")