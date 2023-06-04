from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField,SelectMultipleField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class SearchForm(FlaskForm):

    first_name = StringField(label = "User's first name")

    last_name = StringField(label = "User's last name")

    category= SelectField(label="Categories", 
                                     choices = [('', 'None'),
                                                ('drama', 'Drama'),
                                                ('novel', 'Novel'),
                                                ('fiction', 'Fiction'),
                                                ('comedy', 'Comedy'),
                                                ('horror', 'Horror'),
                                                ('romance', 'Romance'),
                                                ('action and adventure', 'Action and Adventure'),
                                                ('classic', 'Classic'),
                                                ('science fiction', 'Science Fiction'),
                                                ('history', 'History'),
                                                ('science', 'Science'),
                                                ('technology', 'Technology'),
                                                ('cooking', 'Cooking'),
                                                ('children book', 'Children Book'),
                                                ('comic', 'Comic'),
                                                ('graphic novel', 'Graphic Novel'),
                                                ('mystery', 'Mystery'),
                                                ('fantasy', 'Fantasy'),
                                                ('historical fiction', 'Historical Fiction'),
                                                ('literary fiction', 'Literary Fiction'),
                                                ('short story', 'Short Story'),
                                                ('thriller', 'Thriller'),
                                                ('memoir', 'Memoir'),
                                                ('poetry', 'Poetry'),
                                                ('self help', 'Self Help'),
                                                ('true crime', 'True Crime'),
                                                ('economics', 'Economics')
                                            ]

    )

    submit = SubmitField("Create")

class UserForm(FlaskForm):

    first_name = StringField(label = "User's first name")

    last_name = StringField(label = "User's last name")

    median_review = StringField(label = "Average review score")

    submit = SubmitField("Create")

class CategoryForm(FlaskForm):
    
    median_review = StringField(label = "Average review score")

    submit = SubmitField("Create")