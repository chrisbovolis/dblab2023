from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import app, db ## initially created by __init__.py, need to be used here
from dbdemo.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()## This is an object of a class that inherits FlaskForm
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
    if(request.method == "POST" and form.validate_on_submit()):
        role_selected = False
        if request.form.get('user-role') == 'User':
            role_selected = True
            loginuser = form.__dict__
            query = "SELECT userid FROM user WHERE username = '{}' AND password = '{}';".format(loginuser['username'].data, loginuser['password'].data)
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                result = cur.fetchone()  # Fetch the result

                if result:  # Check if a valid userid is found
                    db_userid = result[0]  # Extract the userid from the result
                    flash("User logged in successfully", "success")
                    return redirect("/user/{}".format(db_userid)) 
                
                flash("Invalid username or password or role ", "danger")
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        elif request.form.get('user-role') == 'Operator':
            role_selected = True
            loginuser = form.__dict__
            query = "SELECT userid FROM operator WHERE username = '{}' AND password = '{}';".format(loginuser['username'].data, loginuser['password'].data)
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                result = cur.fetchone()  # Fetch the result

                if result:  # Check if a valid userid is found
                    db_userid = result[0]  # Extract the userid from the result
                    flash("Operator logged in successfully", "success")
                    return redirect("/op/{}".format(loginuser['username'].data))  # Redirect to "/user" page
                
                flash("Invalid username or password or role ", "danger")
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        elif request.form.get('user-role') == 'Main Operator':
            role_selected = True
            loginuser = form.__dict__
            query = "SELECT userid FROM main_operator WHERE username = '{}' AND password = '{}';".format(loginuser['username'].data, loginuser['password'].data)
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                result = cur.fetchone()  # Fetch the result

                if result:  # Check if a valid userid is found
                    db_userid = result[0]  # Extract the userid from the result
                    flash("Main operator logged in successfully", "success")
                    return redirect('/centop')  # Redirect to "/user" page
                
                flash("Invalid username or password or role ", "danger")
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        if not role_selected:
            flash("Please select a role.", "danger")
    ## when the form is submitted
    return render_template("login.html", form=form,pageTitle = "Login Page")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500