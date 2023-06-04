from flask_wtf import FlaskForm
from wtforms import StringField,SelectMultipleField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class WritersbybookcatForm(FlaskForm):
    categories= SelectField(label="Categories", validators=[DataRequired(message="Categories is a required field.")],
                                     choices = [
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