from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
import sys
import hashlib

app = Flask(__name__)

def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        try:
            con = sql.connect(".\\databases\\user.db")  
            con.row_factory = sql.Row  
            cur = con.cursor()  
            cur.execute("select userID from UserID where mailID = \'{}\'".format(mail))  
            rows = cur.fetchall()
            #print(rows[0], rows[1])
            for r in rows:
                print("userid:{}".format(r[0]))
                userID = r[0]
            cur.execute("select password from password where userID = \'{}\'".format(userID))
            rows = cur.fetchall()
            for r in rows:
                print("password: {}".format(r[0]))
                hashedPass = r[0]
            if getHash(mail + '-' + password) == hashedPass:
                msg = "success"
            else:
                msg = "wrong mailID or password"
        except:
            msg = "error 5xx"
            print(sys.exc_info())
        finally:
            return msg
        
@app.route('/register', methods = ['POST', 'GET'])
def registerUser():
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
        except:
            con.rollback()
            msg = "error in insert operation"
            print(sys.exc_info())
      
        finally:
         #return render_template("result.html",msg = msg)
            con.close()
        
    return msg
        
#    return "FAILURE"

if __name__ == "__main__":
    app.run(debug = True)
    