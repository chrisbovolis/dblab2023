from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_book.forms import OpBookForm, LessOpBookForm

from dbdemo.op_book import op_book

@op_book.route("/op/<username>/books")
def getBooksop(username):
    """
    Retrieve books from database
    """
    try:
        form = OpBookForm()
        cur = db.connection.cursor()
        query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.username = '{}';".format(username)
        cur.execute(query)
        schoolid = cur.fetchone()
        query="SELECT * FROM books b INNER JOIN bookinlib bl ON b.bookid=bl.bookid WHERE bl.schoolid='{}';".format(schoolid[0])
        cur.execute("SELECT * FROM books b INNER JOIN bookinlib bl ON b.bookid=bl.bookid WHERE bl.schoolid='{}';".format(schoolid[0]))
        column_names = [i[0] for i in cur.description]
        print("Query:",query)
        books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print("something")
        print(books[0])
        for book in books:
            print("HELLO")
            query = "SELECT w.first_name, w.last_name FROM writer w JOIN bookswriter bw ON w.wrid = bw.wrid WHERE bw.bookid = {};".format(book['bookid'])
            cur.execute(query)
            writer = cur.fetchone()
            print("Book ID:", book['bookid'])
            print("Query:", writer[0])
            book['writerfirstname'] = writer[0]
            book['writerlastname'] = writer[1]
            #book['categories']=writer[0]
            #book['keywords']=writer[1]
        for book in books:
            query = "SELECT name FROM category c JOIN bookscategory bc ON c.catid = bc.catid WHERE bc.bookid = {};".format(book['bookid'])
            cur.execute(query)
            categories = cur.fetchall()
            book['categories'] = categories
            print("here",categories)
        for book in books:
            query = "SELECT name FROM keyword k JOIN bookskeywords bk ON k.kwid = bk.kwid WHERE bk.bookid = {};".format(book['bookid'])
            cur.execute(query)
            keywords = cur.fetchall()
            book['keywords'] = keywords
            print("here2",schoolid)
        for book in books:
            query = "SELECT cpavail FROM bookinlib WHERE schoolid = {} AND bookid='{}';".format(schoolid[0],book['bookid'])
            print("query",query)
            cur.execute(query)
            cpavail = cur.fetchone()
            book['cpavail'] = cpavail[0]
            print("query",query)
            print("here3",cpavail)
        for book in books:
            query = "SELECT cptotal FROM bookinlib WHERE schoolid = {} AND bookid='{}';".format(schoolid[0],book['bookid'])
            cur.execute(query)
            cptotal = cur.fetchone()
            book['cptotal'] = cptotal[0]
            print("here4",cptotal)
        cur.close()
        print("book",books[:])
        return render_template("op_books.html",  books = books, username=username, pageTitle = "Books Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@op_book.route("/op/<username>/books/create", methods = ["GET", "POST"]) ## "GET" by default
def createBookop(username):
    """
    Create new book in the database
    """
    form = OpBookForm() ## This is an object of a class that inherits FlaskForm
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
                print("found book",book_id)
                #find schoolid
                query3="SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON o.schoolid=s.schoolid WHERE o.username='{}'".format(username)
                cur.execute(query3)
                school_id = cur.fetchone()[0]

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

                #insert in bookinlib
                query12="INSERT INTO bookinlib VALUES (null, '{}', '{}','{}','{}')".format(newBook['cpavail'].data,newBook['cptotal'].data,book_id,school_id)
                cur.execute(query12)
                db.connection.commit()
                
                cur.close()
                flash("Book inserted successfully", "success")
                return redirect(url_for("index2",username=username))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_op_book.html", username=username, pageTitle = "Create Book", form = form)


@op_book.route("/op/<username>/books/update/<bookid>", methods = ["POST"])
def updateBookop(username,bookid):
    print("bookid",bookid)
    form = LessOpBookForm() ## see createStudent for explanation
    updateData = form.__dict__
    print("OOOOOH")
    if(form.validate_on_submit()):
        try:
            query1 = "UPDATE books SET title = '{}',publisher='{}',ISBN='{}', pgnum='{}', summary='{}', img='{}', lang='{}' WHERE bookid = '{}';".format(updateData['title'].data,updateData['publisher'].data,updateData['ISBN'].data,updateData['pgnum'].data,updateData['summary'].data,updateData['img'].data,updateData['lang'].data,bookid)
            print("query",query1)
            query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.username = '{}';".format(username)
            cur = db.connection.cursor()
            cur.execute(query)
            schoolid = cur.fetchone()
            query2 = "UPDATE bookinlib SET cpavail='{}',cptotal='{}' WHERE schoolid = '{}' AND bookid='{}';".format(updateData['cpavail'].data,updateData['cptotal'].data,schoolid[0],bookid)
            cur.execute(query1)
            db.connection.commit()
            cur.execute(query2)
            db.connection.commit()
            query4="UPDATE writer w  INNER JOIN bookswriter bw ON bw.wrid=w.wrid SET w.first_name = '{}', w.last_name = '{}' WHERE bw.bookid = '{}';".format(updateData['writerfirstname'].data, updateData['writerlastname'].data,bookid)
            print("query4",query4)
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
    return redirect(url_for("op_book.getBooksop", username=username))

@op_book.route("/op/<username>/books/delete/<bookid>", methods = ["POST"])
def deleteBook2(username,bookid):
    """
    Delete user by id from database
    """
    query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.username = '{}';".format(username)
    cur = db.connection.cursor()
    cur.execute(query)
    schoolid = cur.fetchone()
    print("query",query)
    query = "DELETE FROM bookinlib WHERE schoolid = '{}' AND bookid='{}';".format(schoolid[0],bookid)
    print("query",query)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Book deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("op_book.getBooksop", username=username))