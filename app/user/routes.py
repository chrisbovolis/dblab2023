from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.user.forms import UserForm
from dbdemo.user import user

@user.route("/users")
def getUsers():
    """
    Retrieve users from database
    """
    try:
        form = UserForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM user")
        column_names = [i[0] for i in cur.description]
        users = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("users.html", users = users, pageTitle = "Users Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@user.route("/users/create", methods = ["GET", "POST"]) ## "GET" by default
def createUser():
    """
    Create new user in the database
    """
    form = UserForm() ## This is an object of a class that inherits FlaskForm
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
        newUser = form.__dict__
        query = "INSERT INTO user VALUE (null,'{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(newUser['first_name'].data,newUser['last_name'].data,newUser['username'].data,newUser['schoolid'].data,newUser['password'].data,newUser['status'].data,newUser['birthdate'].data,newUser['num_lent'].data,newUser['num_reserved'].data,newUser['punctual'].data,newUser['email'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("User inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_user.html", pageTitle = "Create User", form = form)

@user.route("/users/update/<int:userid>", methods = ["POST"])
def updateUser(userid):
    """
    Update a user in the database, by id
    """
    form = UserForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE user SET first_name = '{}',last_name='{}',username='{}',schoolid='{}',password='{}',status='{}', birthdate='{}', num_lent='{}', num_reserved='{}', punctual='{}',email='{}' WHERE userid = {};".format(updateData['first_name'].data,updateData['last_name'].data,updateData['username'].data,updateData['schoolid'].data,updateData['password'].data,updateData['status'].data,updateData['birthdate'].data,updateData['num_lent'].data,updateData['num_reserved'].data,updateData['punctual'].data,updateData['email'].data,userid)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("User updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("user.getUsers"))

@user.route("/users/delete/<int:userid>", methods = ["POST"])
def deleteUser(userid):
    """
    Delete user by id from database
    """
    query = "DELETE FROM user WHERE userid = {};".format(userid)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("User deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("user.getUsers"))