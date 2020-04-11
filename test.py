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
    # return render_template("home.html")
    return "hey"
@app.route('/search')
def search():
    # res = ""
    # res2 = ""
    # if request.method == 'POST':
        # searchSTR = request.form['search']
        # print(searchSTR)
    N = 2
    df = pd.read_csv(".\\databases\\song_info.csv")
    _df = pd.DataFrame( data = {'songName' : list(df.head(N).song_name), 'artistName': list(df.head(N).artist_name), 'link' : ['link']*N } ) 
    print(_df.to_html())

    return render_template('test.html', tables =  [_df.to_html(header = False, index = False)], titles = ['song name', 'Artist', ''])

if __name__ == "__main__":
    app.run(debug = True)
    # df = pd.read_csv(".\\databases\\song_info.csv")
    # _df = pd.DataFrame( data = {'songName' : list(df.head(N).song_name), 'artistName': list(df.head(N).artist_name), 'link' : ['link']*N } ) 
    # print(_df.to_html())
    
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
    