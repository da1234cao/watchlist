import os
import click
import time
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_connect')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()

    message = Message(name='hello', body='message')
    db.session.add(message)
    db.session.commit()

    click.echo("Done.")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 用户名
    body = db.Column(db.String(150))  # 留言
    time = db.Column(db.DateTime, nullable=True)  # 留言时间

    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        body = request.form.get('message')

        if not name or not body or len(body) > 150:
            flash('Invalid input')
            return redirect(url_for('index'))

        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()

    messages = Message.query.all()
    return render_template('index.html', messages=messages)
