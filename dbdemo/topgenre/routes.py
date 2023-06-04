from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.topgenre import topgenre


        
@topgenre.route("/topgenre", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT c1.name as genre1, c2.name as genre2, COUNT(*) as appearances FROM category c1 INNER JOIN bookscategory bc1 ON bc1.catid=c1.catid INNER JOIN bookscategory bc2 ON bc2.bookid=bc1.bookid INNER JOIN category c2 ON bc2.catid = c2.catid INNER JOIN bookinlib b ON b.bookid = bc1.bookid INNER JOIN lending l ON l.relid = b.relid WHERE c1.name<c2.name GROUP BY c1.name,c2.name ORDER BY appearances DESC LIMIT 3;")
        column_names = [i[0] for i in cur.description]
        topgenre = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()    
        return render_template("topgenre.html", topgenre = topgenre, pageTitle = "Search results")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)