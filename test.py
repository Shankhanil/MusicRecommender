from Recommender import Recommender
import pandas as pd

from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session


'''
app = Flask(__name__)
# Session(app)
# Session(app)

# app.SECRET_KEY = b'\xdch\x87\x1f\x97\x90\xec\xed\x15O\xef]X\x1eU\xa9\x06\xb6\x0e\x13s\xd3\x95\x07'

@app.route('/set')
def set():
    session['key'] = 'abc'
    return 'ok'

@app.route('/get')
def get():
    # session['key'] = 'value'
    return session.get('key', 'NOT SET')
'''
if __name__ == "__main__":
    rc = Recommender(userID = 1)
    # rc.recommend()
    
    rc.listenToSong(song = 'God\'s Plan')
    '''
    rc.listenToSong(song = 'Closer')
    rc.listenToSong(song = 'Believer')
    rc.listenToSong(song = 'Rap God')
    '''
    # rc.listenToSong(song = 'Numb')
    rc.recommend()
    
    
    
    