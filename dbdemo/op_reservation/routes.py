from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_reservation.forms import ReservationForm
from dbdemo.op_reservation.forms import InsertReservationForm
from dbdemo.op_reservation import op_reservation
from dbdemo.op_lending import op_lending

@op_reservation.route("/op/<username>/reservations")
def getReservations(username):
    """
    Retrieve reservations from database
    """
    try:
        form = ReservationForm()
        cur = db.connection.cursor()
        cur.execute("SELECT r.resid,r.start_date,r.due_date,r.reservation_date,r.userid,r.relid,r.active FROM reservation r INNER JOIN bookinlib bl ON r.relid = bl.relid INNER JOIN operator o ON o.schoolid = bl.schoolid WHERE o.username = '{}' ;".format(username))
        column_names = [i[0] for i in cur.description]
        op_reservations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        print("reservations",op_reservations)
        return render_template("op_reservations.html", op_reservations = op_reservations, username=username, pageTitle = "Reservations Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@op_reservation.route("/op/<username>/reservations/create", methods = ["GET", "POST"]) ## "GET" by default
def createReservation(username):
    """
    Create new reservation in the database
    """
    form = InsertReservationForm() ## This is an object of a class that inherits FlaskForm
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
        new_op_Reservation = form.__dict__
        print("real user id",form['userid'].data)
        query1 = "SELECT num_reserved,status,schoolid,punctual FROM user WHERE userid = '{}'".format(form['userid'].data)
        cur = db.connection.cursor()
        cur.execute(query1)
        data  = cur.fetchone()
        cur.execute("SELECT schoolid FROM bookinlib WHERE relid = {};".format(form['relid'].data))
        result = cur.fetchone()
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        result2 = cur.fetchone()
        if(data is None or (data[1] == 'teacher'and data[0]>=1 )or(data[1] == 'student'and data[0]>=2 )):
            flash("Cannot reserve books '{}'".format(query1), "danger")
        elif(result is None or(result[0]!= data[2])):
            flash("Book not in library", "danger")
        elif((result2[0]!= result[0]) or (result2[0]!= data[2])):
            flash("Book or User not in your library", "danger")
        elif(data[3] != 1):
            flash("The User is not allowed to lend", "danger")
        else:
            query = "INSERT INTO reservation (resid, userid, relid) VALUE (null, '{}', '{}');".format(new_op_Reservation['userid'].data,new_op_Reservation['relid'].data)
            print("query",query)
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Reservation inserted successfully", "success")
                return redirect(url_for("index2",username = username))
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        
    ## else, response for GET request
    return render_template("create_reservation_op.html", username=username, pageTitle = "Create Reservation", form = form)

@op_reservation.route("/op/reservations/update/<int:resid>", methods = ["POST"])
def updateReservation(resid):
    """
    Update a reservation in the database, by id
    """
    form = ReservationForm() ## see createStudent for explanation
    updateData = form.__dict__
    cur = db.connection.cursor()
    booksc = None
    
    if(form.validate_on_submit()):
        query1 = "SELECT num_lent,status,schoolid FROM user WHERE userid = '{}'".format(form['userid'].data)
        cur = db.connection.cursor()
        cur.execute(query1)
        data  = cur.fetchone()
        print("data",query1)
        cur.execute("SELECT schoolid FROM bookinlib WHERE relid = {};".format(form['relid'].data))
        result = cur.fetchone()
        print("result",result)
        cur.execute("SELECT o.username FROM operator o INNER JOIN bookinlib bl ON bl.schoolid = o.schoolid INNER JOIN reservation l ON l.relid = bl.relid WHERE l.resid ={}".format(resid))
        username = cur.fetchone()[0]
        print("username",username)
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        result2 = cur.fetchone()
        if(data is None or result is None or(result[0]!= data[2])):
            #print("user's school",data[2])
            #print("book's school",result[0])
            flash("Book and User not in the same library", "danger")
        elif((result2[0]!= result[0]) or (result2[0]!= data[2])):
            flash("Book or User not in your library", "danger")
        else:
            if((form['start_date'].data == '' or form['start_date'].data == 'None') and (form['due_date'].data == '' or form['due_date'].data == 'None') and (form['active'].data == '' or form['active'].data == 'None')):
                query = "UPDATE reservation SET start_date = NULL, due_date=NULL,reservation_date='{}',userid = '{}', relid = '{}', active = 0 WHERE resid = {};".format(updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,resid)
            elif((form['start_date'].data == '' or form['start_date'].data == 'None') and (form['due_date'].data == '' or form['due_date'].data == 'None')):
                query = "UPDATE reservation SET start_date = NULL, due_date=NULL,reservation_date='{}',userid = '{}', relid = '{}', active = '{}' WHERE resid = {};".format(updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['active'].data,resid)
            elif((form['start_date'].data == '' or form['start_date'].data == 'None') and (form['active'].data == '' or form['active'].data == 'None')):
                query = "UPDATE reservation SET start_date = NULL, due_date='{}',reservation_date='{}',userid = '{}', relid = '{}', active = 0 WHERE resid = {};".format(updateData['due_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,resid)
            elif((form['due_date'].data == '' or form['due_date'].data == 'None') and (form['active'].data == '' or form['active'].data == 'None')):
                query = "UPDATE reservation SET start_date = '{}', due_date=NULL,reservation_date='{}',userid = '{}', relid = '{}', active = 1 WHERE resid = {};".format(updateData['start_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,resid)
            elif((form['start_date'].data != '' and form['start_date'].data != 'None') and (form['active'].data == '' or form['active'].data == 'None')):
                query = "UPDATE reservation SET start_date = '{}', due_date='{}',reservation_date='{}',userid = '{}', relid = '{}', active = 1 WHERE resid = {};".format(updateData['start_date'].data,updateData['due_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,resid)
            elif(form['start_date'].data == '' or form['start_date'].data == 'None'):
                query = "UPDATE reservation SET start_date = NULL, due_date='{}',reservation_date='{}',userid = '{}', relid = '{}', active = '{}' WHERE resid = {};".format(updateData['due_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['active'].data,resid)
            elif(form['due_date'].data == '' or form['due_date'].data == 'None'):
                query = "UPDATE reservation SET start_date = '{}', due_date=NULL,userid = '{}', reservation_date='{}',relid = '{}', active = '{}' WHERE resid = {};".format(updateData['start_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['active'].data,resid)
            else:
                query = "UPDATE reservation SET start_date = '{}', due_date='{}',reservation_date='{}',userid = '{}', relid = '{}',active='{}' WHERE resid = {};".format(updateData['start_date'].data,updateData['due_date'].data,updateData['reservation_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['active'].data,resid)
            
            try:
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Reservation updated successfully", "success")
            except Exception as e:
                flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("op_reservation.getReservations",username = username))

@op_reservation.route("/op/reservations/delete/<int:resid>", methods = ["POST"])
def deleteReservation(resid):
    """
    Delete reservation by id from database
    """
    query = "DELETE FROM reservation WHERE resid = {};".format(resid)
    userid ='1'
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT o.userid,o.schoolid FROM operator o INNER JOIN bookinlib bl ON bl.schoolid = o.schoolid INNER JOIN reservation l ON l.relid = bl.relid WHERE l.resid = {}".format(resid))
        username = cur.fetchone()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Reservation deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("op_lending.createOp_Lending",username = username[0]))