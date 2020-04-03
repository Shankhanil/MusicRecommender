from flask import Flask, request, render_template
import sqlite3 as sql
import sys
import hashlib

app = Flask(__name__)

def isValid(mail, age):
    return False

@app.route('/register', methods = ['POST', 'GET'])
def registerUser():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        password = request.form['password']
        age = request.form['age']
        if isValid(mail, age) == True:
            return "True"
        
    return "FAILURE"

if __name__ == "__main__":
    app.run(debug = True)
    