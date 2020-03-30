from flask import Flask
app = Flask(__name__)

@app.route('/login', method = ['POST', 'GET'])
def f(name):
    if request.method == 'POST':
        user = request.form['nm']
    return user

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)
