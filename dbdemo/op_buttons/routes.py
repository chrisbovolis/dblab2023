from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here

from dbdemo.op_buttons import op_buttons





@op_buttons.route("/operator/delete/expired/<username>", methods = ["POST"])
def delexpreserv(username):
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        schoolid = cur.fetchone()[0]
        cur.execute("DELETE r FROM reservation r INNER JOIN bookinlib bl ON r.relid = bl.relid WHERE bl.schoolid = '{}' AND r.active = 1 AND r.due_date < CURRENT_DATE();".format(schoolid))
        db.connection.commit()
        cur.close()
        flash("Expired reservations deleted", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("index2",username= username))

@op_buttons.route("/operator/punctual/<username>", methods = ["POST"])
def punctual(username):
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        schoolid = cur.fetchone()[0]
        cur.execute("UPDATE user u INNER JOIN lending l ON l.userid = u.userid SET u.punctual = 0 WHERE u.schoolid = '{}' AND l.due_date < CURRENT_DATE();".format(schoolid))
        db.connection.commit()
        cur.close()
        flash("Users with late returns marked", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("index2",username= username))

@op_buttons.route("/operator/waitingreservation/<username>", methods = ["POST"])
def reserve(username):
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT schoolid FROM operator WHERE username = '{}';".format(username))
        schoolid = cur.fetchone()[0]
        cur.execute("SELECT r.relid, COUNT(*) AS reservation_count, b.cpavail FROM reservation AS r JOIN bookinlib AS b ON r.relid = b.relid WHERE b.cpavail > 0 AND b.schoolid = '{}' AND r.active = 0 GROUP BY r.relid, b.cpavail;".format(schoolid))
        books = cur.fetchall()
        for book in books:
            print(book)
            cur.execute("UPDATE reservation AS r JOIN ( SELECT resid FROM reservation WHERE relid = {} AND active = 0 ORDER BY reservation_date LIMIT {} ) AS subquery ON r.resid = subquery.resid SET r.active = true, r.start_date = CURRENT_TIMESTAMP, r.due_date = TIMESTAMPADD(DAY, 7, NOW());".format(book[0],min(book[1],book[2])))
        db.connection.commit()
        cur.close()
        flash("Reservations are updated", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("index2",username= username))