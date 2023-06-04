from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.operator.forms import OperatorForm
from dbdemo.operator import operator

@operator.route("/operators")
def getOperators():
    """
    Retrieve operators from database
    """
    try:
        form = OperatorForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM operator")
        column_names = [i[0] for i in cur.description]
        operators = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("operators.html", operators = operators, pageTitle = "Operators Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@operator.route("/operators/create", methods = ["GET", "POST"]) ## "GET" by default
def createOperator():
    """
    Create new operator in the database
    """
    form = OperatorForm() ## This is an object of a class that inherits FlaskForm
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
        newOperator = form.__dict__
        query = "INSERT INTO operator VALUE (null,'{}', '{}', '{}','{}','{}','{}');".format(newOperator['first_name'].data,newOperator['last_name'].data,newOperator['username'].data,newOperator['password'].data,newOperator['schoolid'].data,newOperator['email'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Operator inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_operator.html", pageTitle = "Create Operator", form = form)

@operator.route("/operators/update/<int:userid>", methods = ["POST"])
def updateOperator(userid):
    """
    Update a operator in the database, by id
    """
    form = OperatorForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE operator SET first_name = '{}',last_name='{}',username='{}',password='{}',schoolid='{}',email='{}' WHERE userid = {};".format(updateData['first_name'].data,updateData['last_name'].data,updateData['username'].data,updateData['password'].data,updateData['schoolid'].data,updateData['email'].data,userid)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Operator updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("operator.getOperators"))

@operator.route("/operators/delete/<int:userid>", methods = ["POST"])
def deleteOperator(userid):
    """
    Delete operator by id from database
    """
    query = "DELETE FROM operator WHERE userid = {};".format(userid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Operator deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("operator.getOperators"))