from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.user_review.forms import UserReviewForm,UserBookidForm,UserReviewShowForm
from dbdemo.user_review import user_review

@user_review.route("/user/<int:userid>/reviews", methods = ["GET", "POST"])
def getreviews(userid):
    """
    Create new school in the database
    """
    form = UserBookidForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain user input, w[hereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
            try:
                form2 = UserReviewShowForm()
                cur = db.connection.cursor()
                cur.execute("SELECT b.bookid FROM books b JOIN bookinlib bil ON bil.bookid = b.bookid WHERE bil.relid = {};".format(form['bookid'].data))
                bookid = cur.fetchone()
                cur.execute("SELECT * FROM review WHERE bookid = {};".format(bookid[0]))   
                column_names = [i[0] for i in cur.description]
                reviews = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                for review in reviews:
                    review['bookid'] = form['bookid'].data
                cur.close()
                
                return render_template("user_reviews.html", reviews = reviews, userid=userid, pageTitle = "Search results", form=form2)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("review_search.html", userid=userid, pageTitle = "Filters to search review of a book", form = form)

@user_review.route("/user/<int:userid>/reviews/create", methods = ["GET", "POST"]) ## "GET" by default
def createreview(userid):
    """
    Create new review in the database
    """
    form = UserReviewForm() ## This is an object of a class that inherits FlaskForm
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
        newreview = form.__dict__
        cur = db.connection.cursor()
        booksc = None
        cur.execute("SELECT schoolid FROM bookinlib WHERE relid = {};".format(form['bookid'].data))
        result = cur.fetchone()

        if result is None:
            flash("Book not in library", "danger")
        else:
            booksc = result[0]

        cur.execute("SELECT schoolid FROM user WHERE userid = {};".format(userid))
        usersc = cur.fetchone()[0]
        if(usersc == booksc):
            cur.execute("SELECT b.bookid FROM books b JOIN bookinlib bil ON bil.bookid = b.bookid WHERE bil.relid = {};".format(form['bookid'].data))
            bookid = cur.fetchone()
            query = "INSERT INTO review (reviewid, text, bookid, userid, scale ) VALUE (null,'{}', '{}','{}','{}');".format(newreview['text'].data,bookid[0],userid,newreview['scale'].data)
            try:
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Review inserted successfully", "success")
                return redirect(url_for("index3",userid=userid))
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        else:
            cur.close()
            flash("Book not in library", "danger")

    ## else, response for GET request
    return render_template("create_review_user.html", userid=userid, pageTitle = "Create review", form = form)

@user_review.route("/user/<int:userid>/reviews/mine", methods = ["GET", "POST"])
def myreviews(userid):
    """
    View my reviews in the database
    """
    form = UserReviewShowForm()
    
    cur = db.connection.cursor()
    cur.execute("SELECT schoolid FROM user WHERE userid = {};".format(userid))
    usersc = cur.fetchone()[0]
    cur.execute("SELECT * FROM review WHERE userid = {};".format(userid))   
    column_names = [i[0] for i in cur.description]
    reviews = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    for review in reviews:
        cur.execute("SELECT relid FROM bookinlib WHERE bookid = {} AND schoolid = {};".format(review['bookid'],usersc))
        bookinlibid = cur.fetchone()[0]
        review['bookid'] = bookinlibid
    cur.close()
                
    return render_template("myreviews.html", reviews = reviews, userid=userid, pageTitle = "Search results", form=form)
    

@user_review.route("/user/reviews/mine/update/<int:reviewid>", methods = ["POST"])
def updatereview(reviewid):
    """
    Update a review in the database, by id
    """
    form = UserReviewShowForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE review SET text = '{}',scale='{}' WHERE reviewid = {};".format(updateData['text'].data,updateData['scale'].data,reviewid)
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT userid FROM review WHERE reviewid ={}".format(reviewid))
            userid = cur.fetchone()[0]
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Review updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("user_review.myreviews",userid = userid))

@user_review.route("/user/reviews/mine/delete/<int:reviewid>", methods = ["POST"])
def deletereview(reviewid):
    """
    Delete review by id from database
    """
    query = "DELETE FROM review WHERE reviewid = {};".format(reviewid)
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT userid FROM review WHERE reviewid ={}".format(reviewid))
        userid = cur.fetchone()[0]
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Review deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("user_review.myreviews",userid = userid))