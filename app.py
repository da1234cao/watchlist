import click
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 数据库的连接配置放在.env文件中。
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_connect')
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app

app.config['SECRET_KEY'] = 'dev'


# 清空数据库中的表，表结构保留
@app.cli.command()  # 注册命令
def cleardb():
    db.drop_all()
    db.create_all()
    click.echo('Cleared database.')


# 使用一些数据初始化数据库中表
@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()

    user = User(name="dacao", username="dacao")
    user.set_password("1735505")

    movies = [
        {'title': '三毛流浪记', 'year': '1949'},
        {'title': '航海王', 'year': '1999'},
        {'title': 'The Shawshank Redemption', 'year': '1994'},
        {'title': '父母爱情', 'year': '2012'},
        {'title': '美丽人生', 'year': '1997'},
    ]

    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")


# 用户表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


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
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页,url改变，调用get方法，有这行，没这行都行
        # return render_template('index.html') #url不变，这时候渲染，没有获取到user,movie的值

    user = User.query.first()  # 读取第一个用户信息 --》用于base.html
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)


# 修改
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


# 管理员
@app.cli.command()
@click.option('--username', prompt=True, help='The usename used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        # user.password = password  ---》写错了，检测出来
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


# 回调函数
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
            # return redirect(url_for(login)) -->这里测试出来了，当时写错了

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')


# 登出
@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


# 用户修改
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
            # return redirect(url_for('settings.html')) ---》这里我当时写错了，这里检测出来

        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')
