from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
import sys
import hashlib
from Recommender import Recommender

app = Flask(__name__)


def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()


@app.route('/login', methods = ['POST', 'GET'])
def login():
    print("login")
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        msg = "Wrong mail-id or password"
        try:
            con = sql.connect(".\\databases\\user.db")  
            con.row_factory = sql.Row  
            cur = con.cursor()
            
            cur.execute("select userID from UserID where mailID = \'{}\'".format(mail))  
            rows = cur.fetchall()
            
            if len(rows) > 0:
                for r in rows:
                    #print("userid:{}".format(r[0]))
                    userID = r[0]
            
                cur.execute("select password from password where userID = \'{}\'".format(userID))
                rows2 = cur.fetchall()
                
                if len(rows2) > 0:
                    for r in rows2:
                        #print("password: {}".format(r[0]))
                        hashedPass = r[0]
                    if getHash(mail + '-' + password) == hashedPass:
                        msg = "success"
                    else:
                        msg = "fail"
        except:
            msg = "error 5xx"
            print(sys.exc_info())
            return msg
        finally:
            # print(msg)
            if msg == "success":
                return "SUCCESS"
            else:
                return render_template("login.html")
            
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        password = request.form['password']
        age = request.form['age']
        
        #connect to SQL
        try:
            with sql.connect(".\\databases\\user.db") as con:
                cur = con.cursor()
                userID = getHash(name + '-' + mail)
                hashedPass = getHash(mail + '-' + password)
                
                cur.execute("INSERT INTO UserID(UserID, mailID)VALUES (?,?)",( userID, mail))
                cur.execute("INSERT INTO password(UserID, password)VALUES (?,?)",( userID, hashedPass))
                cur.execute("INSERT INTO UserDetails(UserID, name, age) VALUES (?,?, ?)",( userID, name, age))
                
                con.commit()
                
                msg = "Record successfully added"
                return redirect(url_for("login"))
        except:
        
            con.rollback()
            msg = "SOME ERROR OCCURED"
            print(sys.exc_info())
      
        finally:
            con.close()
        
    return msg
        
#    return "FAILURE"

@app.route('/')
def index():
    print("index()")
    #return "<h1>welcome to my server</h1>"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug = True)
    