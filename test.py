from Recommender import Recommender
import pandas as pd

from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session



app = Flask(__name__)
# Session(app)
# Session(app)

# app.SECRET_KEY = b'\xdch\x87\x1f\x97\x90\xec\xed\x15O\xef]X\x1eU\xa9\x06\xb6\x0e\x13s\xd3\x95\x07'

@app.route('/')
def set():
    # session['key'] = 'abc'
    # return 'ok'
    return render_template("home.html")

@app.route('/search', methods = ['POST' , 'GET'])
def search():
    res = ""
    if request.method == 'POST':
        searchSTR = request.form['search']
        # print(searchSTR)
        df = pd.read_csv(".\\databases\\song_info.csv")
        if searchSTR in list( df[df.song_name == searchSTR].song_name ):
            res = searchSTR + " by " + list(df[df.song_name == searchSTR].artist_name)[0]
    return render_template("home.html", search = res)
    # return searchSTR
    # return "abc"
if __name__ == "__main__":
    app.run(debug = True)
    
    
'''
if __name__ == "__main__":
    rc = Recommender(userID = 1)
    # rc.recommend()
    
    rc.listenToSong(song = 'Death Trend Setta')
    rc.listenToSong(song = 'Guerilla Radio')
    
    # 
    rc.listenToSong(song = 'Closer')
    rc.listenToSong(song = 'Believer')
    rc.listenToSong(song = 'Rap God')
    # rc.listenToSong(song = 'Numb')
    rc.recommend()
    
    
'''   
    