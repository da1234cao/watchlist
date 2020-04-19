from flask import Flask, url_for, render_template

from flask_sqlalchemy import SQLAlchemy

import click, os

app = Flask(__name__)

# 数据库的连接配置放在.env文件中。
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_connect')
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app


# 清空数据库中的表，表结构保留
@app.cli.command()  # 注册命令
def cleardb(drop):
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


# 使用一些数据初始化数据库中表
@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()

    name = "dacao"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done")


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


# 电影表
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


# 定义自定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404  # 这里是有两个返回值吗


@app.route('/')
@app.route('/index')
def index():
    user = User.query.first()  # 读取第一个用户信息
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)
