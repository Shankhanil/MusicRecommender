from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import sqlite3 as sql
import sys
import hashlib
import os
from Recommender import Recommender
import pandas as pd
import re


app = Flask(__name__)


def getHash(string):
    res = hashlib.sha256(string.encode())
    return res.hexdigest()

@app.route('/')
def index():
    return redirect(url_for("loginPage"))

@app.route('/listeningHistory')
def listeningHistory():

    return render_template("listeningHistory.html")
    

@app.route('/myAccount')
def myAccount():

    return render_template("account.html")
    
    

@app.route('/logOut')
def logOut():
    session.pop('username', None)
    return render_template("login.html", message = "You've been logged out")

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('loginPage'))
    else:
        param = session['username']
        
    name = param.split('-')[0]
    userID = param.split('-')[1]
    print(name, userID)
    
    rc = Recommender(userID = userID)
    rc.recommend()
    Clustersongs = rc.getRecommendedSongsByCluster()
    Artistsongs = rc.getRecommendedSongsByArtist()
    str2 = ""
    str3 = ""
    
    songListfromCluster = False
    songListfromArtist = False
    if len(Clustersongs) > 0:
        songListfromCluster = True
    if len(Artistsongs) > 0:
        songListfromArtist = True
    
    dfSongCluster = pd.DataFrame( data = {'song_name' : Clustersongs})
    dfSongArtist = pd.DataFrame( data = {'song_name' : Artistsongs})
    return render_template("home.html", name = name, songListfromCluster = songListfromCluster, songListfromArtist = songListfromArtist, \
        tables = [dfSongCluster.to_html(header = False, index = False), dfSongArtist.to_html(header = False, index = False)]\
        , titles = ['name'])

@app.route('/search', methods = ['POST' , 'GET'])
def search():
    res = ""
    res2 = ""
    FLAG = False
    if request.method == 'POST':
        searchSTR = request.form['search']
        print(searchSTR)
        df = pd.read_csv(".\\databases\\song_info.csv")
        
        L = list( df.song_name )

        songL = []
        artistL = []
        for x in L:
            X = re.findall('\A'+searchSTR, x, re.IGNORECASE)
            if(X):
                if x not in songL:
                    songL.append(x)
                    
        for x in songL:
            artistL.append(list(df[df.song_name == x].artist_name)[0])
        
        dfsong = pd.DataFrame(data = { 'song': songL, 'artist': artistL } )
        L = list( df.artist_name )
        
        artistL = []
        for x in L:
            X = re.findall('\A'+searchSTR, x, re.IGNORECASE)
            if(X):
                if x not in artistL:
                    artistL.append(x)
        dfartist = pd.DataFrame(data = {'': [' ']*len(artistL), 'artist': artistL } )
        FLAG = True
    return render_template("_home.html", tables = [dfsong.to_html(header = False, index = False), dfartist.to_html(header = False, index = False)], \
        titles = ['song', 'artist'], \
        FLAG = FLAG)


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
                        
                        hashedPass = r[0]
                    if getHash(mail + '-' + password) == hashedPass:
                        cur.execute("select name from UserDetails where userID = \'{}\'".format(userID))  
                        rows3 = cur.fetchall()
                        for r in rows3:
                        
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
            
            if msg == "success":
                
                return redirect(url_for("home"))
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
                session['username'] = name + "-" + userID
                return redirect(url_for("home"))
                
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
    