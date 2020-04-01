from flask import Flask, request, render_template
import sqlite3 as sql
import sys
import hashlib

app = Flask(__name__)

@app.route('/register', methods = ['POST', 'GET'])
def registerUser():
    if request.method == 'POST':
        try:
            name = request.form['name']
            mailid = request.form['mailid']
            passw = request.form['passw']
            securepassw = hashlib.sha256(passw.encode()).hexdigest()
            print(name, mailid, securepassw)
            with sql.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO user (uname, mailid, passw) VALUES (?, ?, ?)", (name, mailid, securepassw))
                conn.commit()
                msg = "Successfully registered"
        except:
            conn.rollback()
            print(sys.exc_info())
            msg = "Some error occured"
        finally:
            return msg

if __name__ == "__main__":
    app.run(debug = True)