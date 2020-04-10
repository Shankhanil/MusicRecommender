from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import sqlite3 as sql
import sys
import hashlib
import os
from Recommender import Recommender
import pandas as pd
import re

# SESSION_TYPE = 'redis'
app = Flask(__name__)
# Session(app)



def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()

@app.route('/')
def index():
    return redirect(url_for("loginPage"))


@app.route('/logOut')
def logOut():
    session.pop('username', None)
    return render_template("login.html", message = "You've been logged out")

@app.route('/home/<param>')
def home(param):
    name = param.split('-')[0]
    userID = param.split('-')[1]
    print(name, userID)
    
    rc = Recommender(userID = userID)
    rc.recommend()
    Clustersongs = rc.getRecommendedSongsByCluster()
    Artistsongs = rc.getRecommendedSongsByArtist()
    str2 = ""
    str3 = ""
    for s in Clustersongs:
        str2 = str2 + s + "  ,"
    for s in Artistsongs:
        str3 = str3 + s + " , "
    
    # str1 = "<h3>Welcome to SANGEETifyify, {}.</h3>".format(name) 
    
    # return str1 + "<br><br>" + str2
    return render_template("home.html", name = name, songListfromCluster = str2, songListfromArtist = str3)

@app.route('/search', methods = ['POST' , 'GET'])
def search():
    res = ""
    res2 = ""
    if request.method == 'POST':
        searchSTR = request.form['search']
        print(searchSTR)
        df = pd.read_csv(".\\databases\\song_info.csv")
        
        L = list( df.song_name )
        # print (L)
        songL = []
        for x in L:
            X = re.findall('\A'+searchSTR, x, re.IGNORECASE)
            if(X):
                # res = res + x + " by " + list(df[df.song_name == x].artist_name)[0] + ", "
                if x not in songL:
                    songL.append(x)
                    
        for x in songL:
            res = res + x + " by " + list(df[df.song_name == x].artist_name)[0] + ", "
                
        L = list( df.artist_name )
        # print (L)
        artistL = []
        for x in L:
            X = re.findall('\A'+searchSTR, x, re.IGNORECASE)
            if(X):
                # res2 = res2 + x + ", "
                if x not in artistL:
                    artistL.append(x)
        for x in artistL:
            res2 = res2 + x + ", "
    return render_template("home.html", search = res, searchArtist = res2)


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
                            session['username'] = name + "-" + userID
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
                return redirect(url_for("home", param = name + "-"+userID))
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
                
                msg = "Welcome to SANGEETifyify"
                # return redirect(url_for("loginPage"))
                return redirect(url_for("home", param = name + "-"+userID))
                
        except:
        
            con.rollback()
            msg = "SOME ERROR OCCURED"
            print(sys.exc_info())
      
        finally:
            con.close()
            print( msg)
            

@app.route('/loginPage')
def loginPage():
    if 'username' in session:
        # session.pop('username', None)

        # return "logged in as {}".format(session['username'])
        return redirect(url_for('home', param = session['username']))
    return render_template("login.html")

@app.route('/registerPage')
def registerPage():
    return render_template("register.html")
    


if __name__ == "__main__":
    app.secret_key = b'\xdch\x87\x1f\x97\x90\xec\xed\x15O\xef]X\x1eU\xa9\x06\xb6\x0e\x13s\xd3\x95\x07'
    # app.secret_key = 'super secret key'
    app.run(debug = True)
    