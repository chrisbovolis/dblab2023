from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.teachersmostlend import teachersmostlend


        
@teachersmostlend.route("/teachersmostlend", methods = ["GET", "POST"]) ## "GET" by default
def createsearchform1():
    """
    Create new school in the database
    """
    
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT u.userid, u.first_name, u.last_name, COUNT(l.userid) AS lending_count FROM user u USE INDEX (idx_users_status) INNER JOIN lending l ON l.userid = u.userid WHERE u.status = 'teacher' AND u.birthdate >= DATE_SUB(CURDATE(), INTERVAL 40 YEAR) GROUP BY u.userid, u.first_name, u.last_name ORDER BY lending_count DESC;")
        column_names = [i[0] for i in cur.description]
        teachersmostlend = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()    
        return render_template("teachersmostlend.html", teachersmostlend = teachersmostlend, pageTitle = "Search results")
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)