from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.user_lending.forms import UserLendingForm
from dbdemo.user_lending import user_lending

@user_lending.route("/user/<int:userid>/lendings")
def getUserLendings(userid):
    """
    Retrieve lendings from database
    """
    try:
        form = UserLendingForm()
        cur = db.connection.cursor()
        cur.execute("SELECT relid,starting_date,due_date,return_date FROM lending WHERE userid = {}".format(userid))
        column_names = [i[0] for i in cur.description]
        user_lendings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        for lending in user_lendings:
            query = "SELECT b.title FROM books b JOIN bookinlib bil ON bil.bookid = b.bookid WHERE bil.relid = {};".format(lending['relid'])
            cur.execute(query)
            title = cur.fetchone()
            print(title)
            lending['title'] = title
        cur.close()
        return render_template("user_lendings.html", userid=userid, user_lendings = user_lendings, pageTitle = "Lendings Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

