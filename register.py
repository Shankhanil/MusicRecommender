from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
import sys
import hashlib
import os
from Recommender import Recommender

app = Flask(__name__)



def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()


@app.route('/')
def index():
    return redirect(url_for("loginPage"))


@app.route('/welcome/<name>')
def welcome(name):
    rc = Recommender()
    rc.recommend()
    songs = rc.getRecommendedSongs()
    str1 = "<h3>Welcome to sangeetify, {}.</h3>".format(name) 
    str2 = "Here are a few songs for you:\n{}".format(songs)
    return str1 + "<br><br>" + str2

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
                        cur.execute("select name from UserDetails where userID = \'{}\'".format(userID))  
                        rows3 = cur.fetchall()
                        for r in rows3:
                        #print("password: {}".format(r[0]))
                            name = r[0]
            
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
                # return render_template("success.html")
                return redirect(url_for("welcome", name = name))
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
                
                msg = "Welcome to sangeetify"
                # return redirect(url_for("loginPage"))
                return redirect(url_for("welcome", name = name))
                
        except:
        
            con.rollback()
            msg = "SOME ERROR OCCURED"
            print(sys.exc_info())
      
        finally:
            con.close()
            print( msg)
            

@app.route('/loginPage')
def loginPage():
    print("index()")
    return render_template("login.html")

@app.route('/registerPage')
def registerPage():
    return render_template("register.html")
    


if __name__ == "__main__":
    app.run(debug = True)
    