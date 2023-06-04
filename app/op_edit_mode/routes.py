from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.op_edit_mode.forms import PasswordForm
from dbdemo.op_edit_mode import edit_mode


@edit_mode.route("/op/editpass/<int:userid>", methods = ["GET", "POST"]) ## "GET" by default
def editmode(userid):
    """
    Update a operator in the database, by id
    """
    form = PasswordForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        cur = db.connection.cursor()
        query2 = "UPDATE user SET password = '{}' WHERE userid = '{}';".format(form['password'].data,userid)
        try:
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Passwrod changed", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return render_template("edit_mode.html",userid =userid ,pageTitle = "Change Password", form = form)