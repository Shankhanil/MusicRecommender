from Recommender import Recommender
import pandas as pd

from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session

import re


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
    res2 = ""
    if request.method == 'POST':
        searchSTR = request.form['search']
        print(searchSTR)
        df = pd.read_csv(".\\databases\\song_info.csv")
        
        L = list( df.song_name )
        # print (L)
        
        for x in L:
            X = re.findall('\A'+searchSTR, x)
            if(X):
                res = res + x + " by " + list(df[df.song_name == x].artist_name)[0] + ", "
                
        L = list( df.artist_name )
        # print (L)
        artistL = []
        for x in L:
            X = re.findall('\A'+searchSTR, x)
            if(X):
                # res2 = res2 + x + ", "
                if x not in artistL:
                    artistL.append(x)
        for x in artistL:
            res2 = res2 + x + ", "
    return render_template("home.html") #, search = res, searchArtist = res2)

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
    