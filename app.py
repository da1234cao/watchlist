from flask import Flask, url_for, render_template

from flask_sqlalchemy import SQLAlchemy

import click

app = Flask(__name__)

# 数据库直接写在这里不好
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1735505@localhost:3306/watchlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app


@app.cli.command()  # 注册命令
@click.option('--drop', is_flag=True, help='create after drop')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


# 电影表
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
@app.route('/index')
def index():
    user = User.query.first()  # 读取第一个用户信息
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)
