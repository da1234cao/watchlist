from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello():
    return '<h1>Hello totoro!</h1><img src="http://helloflask.com/totoro.gif">'
