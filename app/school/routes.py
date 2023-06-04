from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.school.forms import SchoolForm
from dbdemo.school import school

@school.route("/schools")
def getSchools():
    """
    Retrieve schools from database
    """
    try:
        form = SchoolForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM schoolunit")
        column_names = [i[0] for i in cur.description]
        schools = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("schools.html", schools = schools, pageTitle = "Schools Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@school.route("/schools/create", methods = ["GET", "POST"]) ## "GET" by default
def createSchool():
    """
    Create new school in the database
    """
    form = SchoolForm() ## This is an object of a class that inherits FlaskForm
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
        newSchool = form.__dict__
        query = "INSERT INTO schoolunit VALUE (null,'{}', '{}', '{}','{}','{}','{}');".format(newSchool['schoolname'].data, newSchool['address'].data,newSchool['city'].data,newSchool['tel'].data, newSchool['email'].data,newSchool['director'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("School inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_school.html", pageTitle = "Create School", form = form)

@school.route("/schools/update/<int:schoolid>", methods = ["POST"])
def updateSchool(schoolid):
    """
    Update a school in the database, by id
    """
    form = SchoolForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE schoolunit SET schoolname = '{}',address='{}',city='{}',tel='{}',email='{}',director='{}' WHERE schoolid = {};".format(updateData['schoolname'].data,updateData['address'].data,updateData['city'].data,updateData['tel'].data,updateData['email'].data,updateData['director'].data,schoolid)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("School updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("school.getSchools"))

@school.route("/schools/delete/<int:schoolid>", methods = ["POST"])
def deleteSchool(schoolid):
    """
    Delete school by id from database
    """
    query = "DELETE FROM schoolunit WHERE schoolid = {};".format(schoolid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("School deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("school.getSchools"))