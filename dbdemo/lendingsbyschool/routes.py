from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.lendingsbyschool.forms import LendingsbyschoolForm
from dbdemo.lendingsbyschool import lendingsbyschool


        
@lendingsbyschool.route("/lendingsbyschool", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    form = LendingsbyschoolForm() ## This is an object of a class that inherits FlaskForm
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
                if(form['month'].data != ''):
                    cur.execute("SELECT s.schoolid,s.schoolname, COUNT(*) as numlent FROM schoolunit s INNER JOIN bookinlib b ON s.schoolid = b.schoolid INNER JOIN lending l ON l.relid = b.relid WHERE YEAR(l.starting_date) = {} AND (MONTH(l.starting_date) = {}) GROUP BY s.schoolid;".format(form['year'].data, form['month'].data))
                else:
                     cur.execute("SELECT s.schoolid,s.schoolname, COUNT(*) as numlent FROM schoolunit s INNER JOIN bookinlib b ON s.schoolid = b.schoolid INNER JOIN lending l ON l.relid = b.relid WHERE YEAR(l.starting_date) = {}  GROUP BY s.schoolid;".format(form['year'].data))
                column_names = [i[0] for i in cur.description]
                lendingsbyschool = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                cur.close()
                
                return render_template("lendingsbyschool.html", lendingsbyschool = lendingsbyschool, pageTitle = "Search results", form=form)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("create_lendingsbyschool.html", pageTitle = "Filters to search lendings by school", form = form)

