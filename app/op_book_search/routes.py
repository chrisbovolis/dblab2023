from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_book_search.forms import SearchBookForm,UserBookForm
from dbdemo.op_book_search import op_book_search


        
@op_book_search.route("/op/<username>/op_book_search", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1(username):
    """
    Create new school in the database
    """
    form = SearchBookForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain user input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
            try:
                cur = db.connection.cursor()
                title = form['title'].data
                firstname = form['first_name'].data
                lastname = form['last_name'].data
                category = form['category'].data
                cpavail = form['cpavail'].data
                query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.username = '{}';".format(username)
                cur.execute(query)
                schoolid = cur.fetchone()
                query2="SELECT DISTINCT b.* FROM books b USE INDEX (idx_book_name) INNER JOIN bookinlib bl ON b.bookid=bl.bookid INNER JOIN bookswriter bw ON bw.bookid = b.bookid INNER JOIN writer w ON w.wrid = bw.wrid INNER JOIN bookscategory bc ON bc.bookid = b.bookid INNER JOIN category c ON c.catid = bc.catid WHERE bl.schoolid LIKE '{}' AND b.title LIKE '{}%' AND w.first_name LIKE '{}%' AND w.last_name LIKE '{}%' AND c.name LIKE '{}%' AND bl.cpavail >= '{}';".format(schoolid[0],title,firstname,lastname,category,cpavail)

                cur.execute(query2)
                column_names = [i[0] for i in cur.description]
                books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                for book in books:
                    query = "SELECT w.first_name, w.last_name FROM writer w JOIN bookswriter bw ON w.wrid = bw.wrid WHERE bw.bookid = {};".format(book['bookid'])
                    cur.execute(query)
                    writer = cur.fetchone()

                    book['writerfirstname'] = writer[0]
                    book['writerlastname'] = writer[1]
                for book in books:
                    query = "SELECT name FROM category c JOIN bookscategory bc ON c.catid = bc.catid WHERE bc.bookid = {};".format(book['bookid'])
                    cur.execute(query)
                    categories = cur.fetchall()
                    book['categories'] = categories

                for book in books:
                    query = "SELECT name FROM keyword k JOIN bookskeywords bk ON k.kwid = bk.kwid WHERE bk.bookid = {};".format(book['bookid'])
                    cur.execute(query)
                    keywords = cur.fetchall()
                    book['keywords'] = keywords
                for book in books:
                    query = "SELECT cpavail,cptotal,relid FROM bookinlib WHERE schoolid = {} AND bookid='{}';".format(schoolid[0],book['bookid'])
                    cur.execute(query)
                    cpavail = cur.fetchone()
                    book['cpavail'] = cpavail[0]
                    book['cptotal'] = cpavail[1]
                    book['relid'] = cpavail[2]
                form2 = UserBookForm()
                return render_template("op_disp_books.html", books = books, username=username, pageTitle = "Search results", form=form2)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("op_books_search.html", username=username, pageTitle = "Filters to search specific books", form = form)

