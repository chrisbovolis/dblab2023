from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.review.forms import ReviewForm,BookidForm,ReviewShowForm
from dbdemo.review import review

@review.route("/reviews", methods = ["GET", "POST"])
def getreviews():
    """
    Create new school in the database
    """
    form = BookidForm() ## This is an object of a class that inherits FlaskForm
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
                form2 = ReviewShowForm()
                cur = db.connection.cursor()
                cur.execute("SELECT * FROM review WHERE bookid = {};".format(form['bookid'].data))   
                column_names = [i[0] for i in cur.description]
                reviews = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                cur.close()
                
                return render_template("reviews.html", reviews = reviews, pageTitle = "Search results", form=form2)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("review_search.html", pageTitle = "Filters to search review of a book", form = form)

@review.route("/reviews/create", methods = ["GET", "POST"]) ## "GET" by default
def createreview():
    """
    Create new review in the database
    """
    form = ReviewForm() ## This is an object of a class that inherits FlaskForm
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
        query = "INSERT INTO review (reviewid, text, bookid, userid, scale ) VALUE (null,'{}', '{}','{}','{}');".format(newreview['text'].data,newreview['bookid'].data,newreview['userid'].data,newreview['scale'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Review inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_review.html", pageTitle = "Create review", form = form)

@review.route("/reviews/update/<int:reviewid>", methods = ["POST"])
def updatereview(reviewid):
    """
    Update a review in the database, by id
    """
    form = ReviewShowForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE review SET text = '{}',bookid='{}',userid='{}',scale='{}' WHERE reviewid = {};".format(updateData['text'].data,updateData['bookid'].data,updateData['userid'].data,updateData['scale'].data,reviewid)
        try:
            cur = db.connection.cursor()
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
    return redirect(url_for("review.getreviews"))

@review.route("/reviews/delete/<int:reviewid>", methods = ["POST"])
def deletereview(reviewid):
    """
    Delete review by id from database
    """
    query = "DELETE FROM review WHERE reviewid = {};".format(reviewid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Review deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("review.getreviews"))