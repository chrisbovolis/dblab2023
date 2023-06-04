from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_not_returned.forms import SearchForm,UserForm
from dbdemo.op_not_returned import op_not_returned


        
@op_not_returned.route("/op/<username>/op_not_returned", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1(username):
    """
    Create new school in the database
    """
    form = SearchForm() ## This is an object of a class that inherits FlaskForm
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
                firstname = form['first_name'].data
                lastname = form['last_name'].data
                delay = form['delay'].data
                query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.username = '{}';".format(username)
                cur.execute(query)
                schoolid = cur.fetchone()
                print(delay)
                if(delay == ''):
                     query2="SELECT  DISTINCT u.* FROM user u INNER JOIN lending l ON l.userid = u.userid WHERE u.punctual = 0 AND u.schoolid = '{}' AND u.first_name LIKE '{}%' AND u.last_name LIKE '{}%';".format(schoolid[0],firstname,lastname)
                else:
                     query2="SELECT DISTINCT u.* FROM user u INNER JOIN lending l ON l.userid = u.userid WHERE u.punctual = 0 AND u.schoolid = '{}' AND u.first_name LIKE '{}%' AND u.last_name LIKE '{}%' AND DATEDIFF(CURRENT_DATE , l.due_date) = '{}';".format(schoolid[0],firstname,lastname,delay)

                cur.execute(query2)
                column_names = [i[0] for i in cur.description]
                books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                form2 = UserForm()
                return render_template("op_disp_not_ret.html", books = books, username=username, pageTitle = "Search results", form=form2)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("op_not_ret_search.html", username=username, pageTitle = "Filters to search users with delayed lendings", form = form)

