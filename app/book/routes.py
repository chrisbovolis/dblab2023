from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.book.forms import BookForm, LessBookForm
from dbdemo.book import book

@book.route("/books")
def getBooks():
    """
    Retrieve books from database
    """
    try:
        form = BookForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM books")
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
        cur.close()
        return render_template("books.html", books = books, pageTitle = "Books Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@book.route("/books/create", methods = ["GET", "POST"]) ## "GET" by default
def createBook():
    """
    Create new book in the database
    """
    form = BookForm() ## This is an object of a class that inherits FlaskForm
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
        newBook = form.__dict__
        try: 
                cur = db.connection.cursor()

                #insert in books
                query1 = "INSERT IGNORE INTO books VALUE (null,'{}', '{}', '{}','{}','{}','{}','{}');".format(newBook['title'].data, newBook['publisher'].data,newBook['ISBN'].data,newBook['pgnum'].data, newBook['summary'].data,newBook['img'].data, newBook['lang'].data)
                cur.execute(query1)
                db.connection.commit()

                #insert in writers
                query2= "INSERT IGNORE INTO writer VALUE (null,'{}','{}');".format(newBook['writerfirstname'].data,newBook['writerlastname'].data)
                cur.execute(query2)
                db.connection.commit()

                #find bookid
                query3= "SELECT bookid FROM books WHERE ISBN = '{}'".format(newBook['ISBN'].data)
                cur.execute(query3)
                book_id = cur.fetchone()[0]
                
                #find writerid
                query4="SELECT wrid FROM writer WHERE first_name = '{}' AND last_name = '{}'".format(newBook['writerfirstname'].data, newBook['writerlastname'].data)
                cur.execute(query4)
                writer_id = cur.fetchone()[0]
                
                #insert into bookswriter
                query5="INSERT IGNORE INTO bookswriter (wrid, bookid) VALUES ('{}', '{}')".format(writer_id, book_id)
                cur.execute(query5)
                db.connection.commit()
                
                #categories
                for category in newBook['categories'].data:
                    #insert into category
                    query6="INSERT IGNORE INTO category VALUE (null,'{}');".format(category)
                    cur.execute(query6)
                    db.connection.commit()

                    #find category id
                    query7="SELECT catid FROM category WHERE name = '{}'".format(category)
                    cur.execute(query7)
                    cat_id = cur.fetchone()[0]

                    #insert into bookscategory
                    query8="INSERT IGNORE INTO bookscategory VALUE (null,'{}','{}');".format(cat_id,book_id)
                    cur.execute(query8)
                    db.connection.commit()
                
                #keywords
                for keyword in newBook['keywords'].data:
                    #insert into keyword
                    query9="INSERT IGNORE INTO keyword VALUE (null,'{}');".format(keyword)
                    cur.execute(query9)
                    db.connection.commit()

                    #find category id
                    query10="SELECT kwid FROM keyword WHERE name = '{}'".format(keyword)
                    cur.execute(query10)
                    kw_id = cur.fetchone()[0]

                    #insert into bookscategory
                    query11="INSERT IGNORE INTO bookskeywords VALUE (null,'{}','{}');".format(kw_id,book_id)
                    cur.execute(query11)
                    db.connection.commit()
                
                cur.close()
                flash("Book inserted successfully", "success")
                return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_book.html", pageTitle = "Create Book", form = form)

@book.route("/books/update/<bookid>", methods = ["POST"])
def updateBook(bookid):
    print("bookid",bookid)
    form = LessBookForm() ## see createStudent for explanation
    updateData = form.__dict__
    #print("OOO",updateData)
    if(form.validate_on_submit()):
        try:
            query1 = "UPDATE books SET title = '{}',publisher='{}',ISBN='{}', pgnum='{}', summary='{}', img='{}', lang='{}' WHERE bookid = '{}';".format(updateData['title'].data,updateData['publisher'].data,updateData['ISBN'].data,updateData['pgnum'].data,updateData['summary'].data,updateData['img'].data,updateData['lang'].data,bookid)            
            cur = db.connection.cursor()
            cur.execute(query1)
            db.connection.commit()
            query4="UPDATE writer w  INNER JOIN bookswriter bw ON bw.wrid=w.wrid SET w.first_name = '{}', w.last_name = '{}' WHERE bw.bookid = '{}';".format(updateData['writerfirstname'].data, updateData['writerlastname'].data,bookid)
            cur.execute(query4)
            db.connection.commit()
            cur.close()
            flash("Book updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("book.getBooks"))

@book.route("/books/delete/<int:bookid>", methods = ["POST"])
def deleteBook(bookid):
    """
    Delete book by id from database
    """
    query = "DELETE FROM books WHERE bookid = {};".format(bookid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Book deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("book.getBooks"))