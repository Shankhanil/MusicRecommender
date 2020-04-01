from flask import Flask, request, render_template
import sqlite3 as sql
import sys
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def List():
    conn = sql.connect('test.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM T')
    rows = cur.fetchall()
    
    return render_template("index.html", rows = rows)
    #conn.close()0

@app.route('/login', methods = ['POST', 'GET'])
def f():
    if request.method == 'POST':
        user = request.form['nm']
        print(user)
    return user

if __name__ == '__main__':
    app.debug =True
    app.run(debug = True)
    List()
