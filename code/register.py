from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
import sys
import hashlib

app = Flask(__name__)

def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()

@app.route('/success/<name>')
def sucess():
    return "Welcome to Musicify, %s" % name
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
                #return redirect(url_for('/success',name = name))
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
    