from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.lending.forms import LendingForm
from dbdemo.lending.forms import InsertLendingForm
from dbdemo.lending import lending

@lending.route("/lendings")
def getLendings():
    """
    Retrieve lendings from database
    """
    try:
        form = LendingForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM lending")
        column_names = [i[0] for i in cur.description]
        lendings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("lendings.html", lendings = lendings, pageTitle = "Lendings Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@lending.route("/lendings/create", methods = ["GET", "POST"]) ## "GET" by default
def createLending():
    """
    Create new lending in the database
    """
    form = InsertLendingForm() ## This is an object of a class that inherits FlaskForm
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
        newLending = form.__dict__
        if(newLending['due_date'].data==''): 
         query = "INSERT INTO lending (lendid, userid, relid ) VALUE (null, '{}', '{}');".format(newLending['userid'].data,newLending['relid'].data)
        else:
         query = "INSERT INTO lending (lendid, due_date, userid, relid ) VALUE (null, '{}', '{}', '{}');".format(newLending['due_date'].data,newLending['userid'].data,newLending['relid'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Lending inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
        
    ## else, response for GET request
    return render_template("create_lending.html", pageTitle = "Create Lending", form = form)

@lending.route("/lendings/update/<int:lendid>", methods = ["POST"])
def updateLending(lendid):
    """
    Update a lending in the database, by id
    """
    form = LendingForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE lending SET starting_date = '{}', due_date='{}',userid = '{}', relid = '{}', return_date='{}',returned='{}' WHERE lendid = {};".format(updateData['starting_date'].data,updateData['due_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['return_date'].data,updateData['returned'].data,lendid)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Lending updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("lending.getLendings"))

@lending.route("/lendings/delete/<int:lendid>", methods = ["POST"])
def deleteLending(lendid):
    """
    Delete lenging by id from database
    """
    query = "DELETE FROM lending WHERE lendid = {};".format(lendid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Lending deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("lending.getLendings"))