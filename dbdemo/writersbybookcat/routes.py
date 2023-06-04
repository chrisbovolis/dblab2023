from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.writersbybookcat.forms import WritersbybookcatForm
from dbdemo.writersbybookcat import writersbybookcat


        
@writersbybookcat.route("/writersbybookcat", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    form = WritersbybookcatForm() ## This is an object of a class that inherits FlaskForm
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
                cur.execute("SELECT DISTINCT w.wrid,w.first_name, w.last_name FROM writer w JOIN bookswriter bw ON w.wrid = bw.wrid JOIN books b ON bw.bookid = b.bookid JOIN ( SELECT bc.bookid FROM bookscategory bc JOIN category c USE INDEX (idx_category_name) ON bc.catid = c.catid WHERE c.name = '{}') AS sub ON b.bookid = sub.bookid;".format(form['categories'].data))
                column_names = [i[0] for i in cur.description]
                writersbybookcat = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                cur.close()
                
                return render_template("writersbybookcat.html", writersbybookcat = writersbybookcat, pageTitle = "Search results", form=form)
            except Exception as e:
                ## if the connection to the database fails, return HTTP response 500
                flash(str(e), "danger")
                abort(500)

    ## else, response for GET request
    return render_template("create_writersbybookcat.html", pageTitle = "Filters to find writers with books in a desired category", form = form)
