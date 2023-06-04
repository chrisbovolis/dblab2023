from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_lending.forms import LendingForm
from dbdemo.op_lending.forms import InsertLendingForm, SeachLendingForm
from dbdemo.op_lending import op_lending

@op_lending.route("/op/<username>/lendings", methods = ["GET", "POST"])
def getOp_Lendings(username):
    """
    Retrieve lendings from database
    """
    form2 = SeachLendingForm()
    if(request.method == "POST" and form2.validate_on_submit()):
        try:
            form = LendingForm()
            cur = db.connection.cursor()
            if(form2['userid'].data == ''):
                cur.execute("SELECT l.lendid,l.starting_date,l.due_date,l.userid,l.relid,l.return_date,l.returned FROM lending l INNER JOIN bookinlib bl ON l.relid = bl.relid INNER JOIN operator o ON o.schoolid = bl.schoolid INNER JOIN user u ON u.userid = l.userid WHERE o.username = '{}' AND u.first_name LIKE '{}%' AND u.last_name LIKE '{}%' ;".format(username,form2['first_name'].data,form2['last_name'].data))
            else:
                cur.execute("SELECT l.lendid,l.starting_date,l.due_date,l.userid,l.relid,l.return_date,l.returned FROM lending l INNER JOIN bookinlib bl ON l.relid = bl.relid INNER JOIN operator o ON o.schoolid = bl.schoolid INNER JOIN user u ON u.userid = l.userid WHERE o.username = '{}' AND u.first_name LIKE '{}%' AND u.last_name LIKE '{}%' AND u.userid = '{}' ;".format(username,form2['first_name'].data,form2['last_name'].data,form2['userid'].data))

            column_names = [i[0] for i in cur.description]
            op_lendings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("op_lendings.html", op_lendings = op_lendings, username=username, pageTitle = "Lendings Page", form = form)
        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)
    return render_template("op_lendings_search.html", username=username, pageTitle = "Lendings Page", form = form2)

@op_lending.route("/op/<username>/lendings/create", methods = ["GET", "POST"]) ## "GET" by default
def createOp_Lending(username):
    """
    Create new lending in the database
    """
    form = InsertLendingForm() ## This is an object of a class that inherits FlaskForm
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
        new_op_Lending = form.__dict__
        query1 = "SELECT num_lent,status,schoolid,punctual FROM user WHERE userid = '{}';".format(form['userid'].data)
        cur = db.connection.cursor()
        cur.execute(query1)
        data  = cur.fetchone()
        cur.execute("SELECT schoolid,cpavail FROM bookinlib WHERE relid = {};".format(form['relid'].data))
        result = cur.fetchone()
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        result2 = cur.fetchone()
        print(result2)
        if(data is None or (data[1] == 'teacher'and data[0]>=1 )or(data[1] == 'student'and data[0]>=2 )):
            flash("Cannot lend any more books", "danger")
        elif(result is None or(result[0]!= data[2])):
            flash("Book or User not in library", "danger")
        elif(data[3] != 1):
            flash("The User is not allowed to lend", "danger")
        elif(result[1]==0):
            flash("No more books left", "danger")
        elif((result2[0]!= result[0]) or (result2[0]!= data[2])):
            flash("Book or User not in your library", "danger")
        else:
            if(new_op_Lending['due_date'].data==''): 
              query = "INSERT INTO lending (lendid, userid, relid ) VALUE (null, '{}', '{}');".format(new_op_Lending['userid'].data,new_op_Lending['relid'].data)
            else:
              query = "INSERT INTO lending (lendid, due_date, userid, relid ) VALUE (null, '{}', '{}', '{}');".format(new_op_Lending['due_date'].data,new_op_Lending['userid'].data,new_op_Lending['relid'].data)
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Lending inserted successfully", "success")
                return redirect(url_for("index2",username=username))
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
            
    ## else, response for GET request
    return render_template("create_lending_op.html", username=username, pageTitle = "Create Lending", form = form)

@op_lending.route("/op/lendings/update/<int:lendid>", methods = ["POST"])
def updateOp_Lending(lendid):
    """
    Update a lending in the database, by id
    """
    form = LendingForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query1 = "SELECT num_lent,status,schoolid,punctual FROM user WHERE userid = {};".format(form['userid'].data)
        cur = db.connection.cursor()
        print("HEEE")
        cur.execute(query1)
        data  = cur.fetchone()
        cur.execute("SELECT schoolid FROM bookinlib WHERE relid = {};".format(form['relid'].data))
        result = cur.fetchone()
        print("SELECT o.username FROM operator o INNER JOIN bookinlib bl ON bl.schoolid = o.schoolid INNER JOIN lending l ON l.relid = bl.relid WHERE l.lendid ={};".format(lendid))
        cur.execute("SELECT o.username FROM operator o INNER JOIN bookinlib bl ON bl.schoolid = o.schoolid INNER JOIN lending l ON l.relid = bl.relid WHERE l.lendid ={};".format(lendid))
        username = cur.fetchone()[0]
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        result2 = cur.fetchone()
        if(data is None or result is None or(result[0]!= data[2])):
            flash("Book or User not in your library", "danger")
        elif((result2[0]!= result[0]) or (result2[0]!= data[2])):
            flash("Book or User not in your library", "danger")
            
        else:
            query = "UPDATE lending SET starting_date = '{}', due_date='{}',userid = '{}', relid = '{}', return_date='{}',returned='{}' WHERE lendid = {};".format(updateData['starting_date'].data,updateData['due_date'].data,updateData['userid'].data,updateData['relid'].data,updateData['return_date'].data,updateData['returned'].data,lendid)
            try:
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Lending updated successfully", "success")
            except Exception as e:
                flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("op_lending.getOp_Lendings",username= username))

@op_lending.route("/op/lendings/delete/<int:lendid>", methods = ["POST"])
def deleteOpLending(lendid):
    """
    Delete lending by id from database
    """
    query = "DELETE FROM lending WHERE lendid = {};".format(lendid)
    username ='1'
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT o.username FROM operator o INNER JOIN bookinlib bl ON bl.schoolid = o.schoolid INNER JOIN lending l ON l.relid = bl.relid WHERE l.lendid = {}".format(lendid))
        username = cur.fetchone()[0]
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Lending deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("op_lending.getOp_Lendings",username=username))
