from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.fivelessthanmax import fivelessthanmax


        
@fivelessthanmax.route("/fivelessthanmax", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT w.wrid,w.first_name, w.last_name,COALESCE(writer_counts.book_count, 0) AS book_count FROM writer w LEFT JOIN ( SELECT bw.wrid, COUNT(bw.bookid) AS book_count FROM bookswriter bw GROUP BY bw.wrid) AS writer_counts ON w.wrid = writer_counts.wrid WHERE (writer_counts.book_count <= ( SELECT MAX(counts) FROM ( SELECT COUNT(*) AS counts FROM bookswriter GROUP BY wrid ORDER BY counts DESC LIMIT 6 ) AS subquery) - 5) OR (w.wrid NOT IN (SELECT DISTINCT wrid FROM bookswriter));")
        column_names = [i[0] for i in cur.description]
        fivelessthanmax = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()    
        return render_template("fivelessthanmax.html", fivelessthanmax = fivelessthanmax, pageTitle = "Search results")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)