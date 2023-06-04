from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

class BookForm(FlaskForm):
    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])

    publisher = StringField(label = "Publisher", validators = [DataRequired(message = "Publisher is a required field.")])

    ISBN = StringField(label = "ISBN", validators = [DataRequired(message = "ISBN is a required field.")])
    
    writerfirstname =StringField(label = "Author's first name", validators = [DataRequired(message = "Author's first name is a required field.")])

    writerlastname =StringField(label = "Author's last name", validators = [DataRequired(message = "Author's last name is a required field.")])

    pgnum = StringField(label = "Number of pages", validators = [DataRequired(message = "Number of pages is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])

    img = StringField(label = "Image")

    categories= SelectMultipleField(label="Categories", validators=[DataRequired(message="Categories is a required field.")],
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

    lang = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])

    keywords= SelectMultipleField(label="Keywords", validators=[DataRequired(message="Keywords is a required field.")],
                                     choices = [('newbook','New Book'),('classic','Classic'),('bestseller',"Bestseller"),('critical','Critically Acclaimed')])
                                               

    submit = SubmitField("Create")

class LessBookForm(FlaskForm):

    title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])

    publisher = StringField(label = "Publisher", validators = [DataRequired(message = "Publisher is a required field.")])

    ISBN = StringField(label = "ISBN", validators = [DataRequired(message = "ISBN is a required field.")])
    
    writerfirstname =StringField(label = "Author's first name", validators = [DataRequired(message = "Author's first name is a required field.")])

    writerlastname =StringField(label = "Author's last name", validators = [DataRequired(message = "Author's last name is a required field.")])

    pgnum = StringField(label = "Number of pages", validators = [DataRequired(message = "Number of pages is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])

    img = StringField(label = "Image")

   
    lang = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])


    submit = SubmitField("Create")