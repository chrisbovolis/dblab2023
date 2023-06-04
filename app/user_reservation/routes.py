from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.user_reservation.forms import UserReservationForm
from dbdemo.user_reservation.forms import InsertUserReservationForm
from dbdemo.user_reservation import user_reservation

@user_reservation.route("/user/<int:userid>/reservations")
def getuser_reservations(userid):
    """
    Retrieve user_reservations from database
    """
    try:
        form = UserReservationForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM reservation WHERE userid = '{}'".format(userid))
        column_names = [i[0] for i in cur.description]
        user_reservations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("user_reservations.html", userid=userid, user_reservations = user_reservations, pageTitle = "Reservations Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@user_reservation.route("/user/<int:userid>/reservation/create", methods = ["GET", "POST"]) ## "GET" by default
def createuser_reservation(userid):
    """
    Create new user_reservation in the database
    """
    form = InsertUserReservationForm() ## This is an object of a class that inherits FlaskForm
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
        query1 = "SELECT num_reserved,status,schoolid FROM user WHERE userid = {}".format(userid)
        cur = db.connection.cursor()
        cur.execute(query1)
        data  = cur.fetchone()
        cur.execute("SELECT schoolid FROM bookinlib WHERE relid = {};".format(form['relid'].data))
        result = cur.fetchone()
        if((data[1] == 'teacher'and data[0]>=1 )or(data[1] == 'student'and data[0]>=2 )):
            flash("Cannot reserve any more books", "danger")
        elif(result is None or(result[0]!= data[2])):
            flash("Book not in library", "danger")
        else:
            newuser_reservation = form.__dict__
            query = "INSERT INTO reservation (resid, userid, relid) VALUE (null, '{}', '{}');".format(userid,newuser_reservation['relid'].data)
            try:
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("user_reservation inserted successfully", "success")
                return redirect(url_for("index3",userid=userid))
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        
    ## else, response for GET request
    return render_template("create_reservation_user.html", userid=userid, pageTitle = "Create reservation", form = form)


@user_reservation.route("/user/reservations/delete/<int:resid>", methods = ["POST"])
def deleteuser_reservation(resid):
    """
    Delete user_reservation by id from database
    """
    userid=-2
    query = "DELETE FROM reservation WHERE resid = {};".format(resid)
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT userid FROM reservation WHERE resid ={}".format(resid))
        userid = cur.fetchone()[0]
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("user_reservation deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("user_reservation.getuser_reservations",userid=userid))