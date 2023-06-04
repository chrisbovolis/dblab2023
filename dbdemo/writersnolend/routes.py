from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.writersnolend import writersnolend


        
@writersnolend.route("/writersnolend", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT w.wrid,w.first_name, w.last_name FROM writer w WHERE w.wrid NOT IN ( SELECT bw.wrid FROM bookswriter bw INNER JOIN bookinlib bl ON bl.bookid = bw.bookid INNER JOIN lending l ON bl.relid = l.relid);")
        column_names = [i[0] for i in cur.description]
        writersnolend = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()    
        return render_template("writersnolend.html", writersnolend = writersnolend, pageTitle = "Search results")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)