from flask import Flask, url_for, render_template, request, flash, redirect

from flask_sqlalchemy import SQLAlchemy

import click, os

app = Flask(__name__)

# 数据库的连接配置放在.env文件中。
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_connect')
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app

app.config['SECRET_KEY'] = 'dev'

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
        {'title': '三毛流浪记', 'year': '1949'},
        {'title': '航海王', 'year': '1999'},
        {'title': 'The Shawshank Redemption', 'year': '1994'},
        {'title': '父母爱情', 'year': '2012'},
        {'title': '美丽人生', 'year': '1997'},
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页,url改变，调用get方法
        # return render_template('index.html') #url不变，这时候渲染，没有获取到user,movie的值

    user = User.query.first()  # 读取第一个用户信息 --》用于base.html
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)


# 修改
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title)> 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)


# 删除
@app.route('/movie/delete/<int:movie_id>')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
