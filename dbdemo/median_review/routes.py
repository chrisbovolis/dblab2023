from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.median_review.forms import SearchForm,UserForm,CategoryForm
from dbdemo.median_review import median_review


        
@median_review.route("/op/<username>/median_review", methods = ["GET", "POST"]) ## "GET" by default
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
                category = form['category'].data
                query = "SELECT s.schoolid FROM schoolunit s INNER JOIN operator o ON s.schoolid=o.schoolid WHERE o.userid = '{}';".format(username)
                cur.execute(query)
                schoolid = cur.fetchone()
                if(firstname == '' and lastname == ''):
                     form2 = CategoryForm()
                     query2 = "SELECT AVG(r.scale) AS median_review FROM review r INNER JOIN bookscategory bc ON r.bookid = bc.bookid INNER JOIN category c ON c.catid = bc.catid WHERE c.name LIKE '{}%';".format(category)
                else:
                     form2 = UserForm()
                     query2 = "SELECT u.userid,u.first_name,u.last_name,AVG(r.scale) AS average_score FROM review r INNER JOIN bookscategory bc ON r.bookid = bc.bookid INNER JOIN user u ON u.userid = r.userid INNER JOIN category c ON c.catid = bc.catid WHERE u.schoolid = '{}' AND u.first_name LIKE '{}%' AND u.last_name LIKE '{}%' AND c.name LIKE '{}%';".format(schoolid[0],firstname,lastname,category)

                cur.execute(query2)
                column_names = [i[0] for i in cur.description]
                books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                if(firstname == '' and lastname == ''):
                    return render_template("op_disp_medianreview2.html", books = books, username=username,pageTitle = "Search results", form=form2)
                else:
                    return render_template("op_disp_medianreview.html", books = books, username=username, pageTitle = "Search results", form=form2)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("op_medianreview_search.html", username=username, pageTitle = "Filters to search the average review score", form = form)

