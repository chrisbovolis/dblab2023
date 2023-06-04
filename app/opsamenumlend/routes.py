from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.opsamenumlend import opsamenumlend
from dbdemo.opsamenumlend.forms import LendingsbyschoolForm


        
@opsamenumlend.route("/opsamenumlend", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    form = LendingsbyschoolForm()
    if(request.method == "POST" and form.validate_on_submit()):
        try:
            cur = db.connection.cursor()
            cur.execute("""
    SELECT o1.userid, o1.first_name, o1.last_name, o1.numlent 
    FROM (
        SELECT o.userid, o.first_name, o.last_name, COUNT(l.relid) AS numlent 
        FROM operator o 
        INNER JOIN bookinlib b ON b.schoolid = o.schoolid 
        INNER JOIN lending l ON l.relid = b.relid 
        WHERE YEAR(l.starting_date) = {}
        GROUP BY o.first_name, o.last_name 
        HAVING COUNT(*) >= 20
    ) AS o1 
    INNER JOIN (
        SELECT numlent 
        FROM (
            SELECT o.first_name, o.last_name, COUNT(l.relid) AS numlent 
            FROM operator o 
            INNER JOIN bookinlib b ON b.schoolid = o.schoolid 
            INNER JOIN lending l ON l.relid = b.relid 
            WHERE YEAR(l.starting_date) = {}
            GROUP BY o.first_name, o.last_name 
            HAVING COUNT(*) >= 20
        ) AS o2 
        GROUP BY numlent 
        HAVING COUNT(*) > 1
    ) AS o2 ON o1.numlent = o2.numlent;
""".format(form['year'].data, form['year'].data))

            column_names = [i[0] for i in cur.description]
            opsamenumlend = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()    
            return render_template("opsamenumlend.html", opsamenumlend = opsamenumlend, pageTitle = "Search results")
        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)
    return render_template("search_same_num_lent.html", pageTitle = "Filters operator lendings by school", form = form)