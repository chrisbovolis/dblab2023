from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError


def validate_password_length(form, field):
    if len(field.data) < 10:
        raise ValidationError('Password must be at least 10 characters long.')
    
    
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


class BookForm(FlaskForm):
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])

    publisher = StringField(label = "Publisher", validators = [DataRequired(message = "Publisher is a required field.")])

    ISBN = StringField(label = "ISBN", validators = [DataRequired(message = "ISBN is a required field.")])
    
    pgnum = StringField(label = "Number of pages", validators = [DataRequired(message = "Number of pages is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])
    
    img = StringField(label = "Image", validators = [DataRequired(message = "Image is a required field.")])

    lang = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])
    submit = SubmitField("Create")


class WriterForm(FlaskForm):
    first_name = StringField(label = "Fist name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    submit = SubmitField("Create")


class UsersForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])
    
    schoolname = StringField(label = "School name", validators = [DataRequired(message = "School name is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])
    
    birthdate = StringField(label = "Date of birth", validators = [DataRequired(message = "Date of birth is a required field.")])

    username = StringField(label = "Username", validators = [DataRequired(message = "Username name is a required field.")])
 
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field."), validate_password_length])
 
    submit = SubmitField("Create")

class LoginForm(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired(message = "Username name is a required field.")])
 
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])
 
    submit = SubmitField("Create")






class MainOperatorForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])
    
    schoolname = StringField(label = "School name", validators = [DataRequired(message = "School name is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    username = StringField(label = "Username", validators = [DataRequired(message = "Username name is a required field.")])
 
    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field."), validate_password_length])
 
    submit = SubmitField("Create")


class CategoryForm(FlaskForm):
    category_name = StringField(label = "Category name", validators = [DataRequired(message = "Category name is a required field.")])

    submit = SubmitField("Create")


class ReserveForm(FlaskForm):
    bookname = StringField(label = "Book name", validators = [DataRequired(message = "Book name is a required field.")])

    userid = StringField(label = "User's ID:", validators = [DataRequired(message = "User's ID is a required field.")])

    submit = SubmitField("Create")


class ReviewForm(FlaskForm):
    bookname = StringField(label = "Book name", validators = [DataRequired(message = "Book name is a required field.")])

    review = StringField(label = "Review")

    scale = SelectField(label="Scale", choices=[('1',), ('2',), ('3',), ('4',), ('5',)], validators=[DataRequired(message="Scale is a required field.")])

    userid = StringField(label = "User's ID:", validators = [DataRequired(message = "User's ID is a required field.")])

    submit = SubmitField("Create")
