# 《flask入门教程》实践
[toc]

## chapter01 准备工作

参考：[要不我们还是用回 virtualenv/venv 和 pip 吧](https://zhuanlan.zhihu.com/p/81568689)

```shell
#流程：

#克隆一个空的仓库
git clone git@github.com:da1234cao/watchlist.git

#charm 打开该仓库目录文件,发现默认的是python2.7
charm watchlist

#包安装
pip3 install virtualenv
sudo apt install python3-venv

#创建虚拟环境watchlist
python3 -m venv watchlist

#激活虚拟环境
source ./watchlist/bin/activate 

#安装flask
(watchlist) pip install flask

#提交仓库
vim .gitignore #创建一个.gitignore
git status; git add; git commit; git push;
```

<br>

<br>

## chapter02 Hello,Flask

在学习语言的时候，验证我们环境的安装情况，我们，通常会输出 ”神奇“的 "hello world"。

此处也是。代码见上面的仓库。

### 环境变量

```shell
#运行flask run,当默认的程序名称不是app.py
export FLASK_APP=XXX

#FLASK_ENV默认为 production 。在开发时，我们需要开启调试模式（ debug mode） 。 
export FLASK_ENV=development 
```

为了不用每次打开新的终端会话都要设置环境变量， 我们安装用来管理系统环境变量的 python-dotenv。

<br>

### URL规则

绑定多个URL、url_for的使用。

**url_for() 函数最简单的用法是以视图函数名作为参数，返回对应的url。**

```python
from flask import url_for

@app.route('/')
def hello():
	return 'Hello'

@app.route('/user/<name>')
def user_page(name):
	return 'User: %s' % name

@app.route('/test')
def test_url_for():
	# 下面是一些调用示例（ 请在命令行窗口查看输出的 URL） ：
	print(url_for('hello')) # 输出： /
	# 注意下面两个调用是如何生成包含 URL 变量的 URL 的
	print(url_for('user_page', name='greyli')) # 输出： /user/greyli
	print(url_for('user_page', name='peter')) # 输出： /user/peter
	print(url_for('test_url_for')) # 输出： /test
	# 下面这个调用传入了多余的关键字参数， 它们会被作为查询字符串附加到 URL后面。
	print(url_for('test_url_for', num=2)) # 输出： /test?num=2
	return 'Test page
```

![image-20200413181735471](README.assets/image-20200413181735471.png)

<br>

<br>

## chapter03 模板

上一章，我们视图函数是这样定义的：

```python
def hello():
	return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
```

但是，**我们的html肯定不是一个字符串可以解决的。**

所以我们得使用html文件。

> 我们把包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板， 执行这些变量替换和逻辑计算工作的过程被称为渲染， 这个工作由我们这一章要学习使用的模板渲染引擎——Jinja2 来完成。

**我们使用render_template() 函数把模板渲染出来。**

```python
@app.route('/')
def index():
	return render_template('index.html', name=name, movies=movies)
```

![image-20200413220709851](README.assets/image-20200413220709851.png)

<br>

<br>

## chapter04 静态文件

上一章是渲染模板。**静态文件（ static files） 和我们的模板概念相反， 指的是内容不需要动态生成的文**
**件。 比如图片、 CSS 文件和 JavaScript 脚本等。**

主要点：**生成静态URL**

```html
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

其他内容是css的部分。我仅仅知道最基本的css,写出来的难看得很。我拷贝了书中的css.

![image-20200414093123006](README.assets/image-20200414093123006.png)

<br>

<br>

## chapter 05 数据库

这章，略微有点多。

**安装数据库工具+设置数据库的URI+创建数据模型+注册命令+增删该查**

### 安装依赖包、连接到数据库

下面用的是root用户登录。当然，最好可以用其他用户登录。

参考：[mysql环境准备](https://blog.csdn.net/sinat_38816924/article/details/105478479)

```shell
#安装依赖包
pip install flask-sqlalchemy
pip install pymysql

#设置数据库URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1*******@localhost:3306/userdb'

#创建数据库
mysql> create database watchlist
```

<br>

### 创建数据模型

```python
# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


# 电影表
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

<br>

### 增删该查

```python
#增加
>>> from app import User, Movie # 导入模型类
>>> user = User(name='Grey Li') # 创建一个 User 记录
>>> m1 = Movie(title='Leon', year='1994') # 创建一个 Movie 记录
>>> m2 = Movie(title='Mahjong', year='1996') # 再创建一个 Movie记录
>>> db.session.add(user) # 把新创建的记录添加到数据库会话
>>> db.session.add(m1)
>>> db.session.add(m2)
>>> db.session.commit() # 提交数据库会话， 只需要在最后调用一次即可

#查
>>> Movie.query.all() # 获取 Movie 模型的所有记录， 返回包含多个模型类实例的列表
>>> Movie.query.filter(Movie.title=='Mahjong').first() # 等同于上面的查询， 但使用不同的过滤方法

#更新
>>> movie = Movie.query.get(2)
>>> movie.title = 'WALL-E' # 直接对实例属性赋予新的值即可
>>> movie.year = '2008'
>>> db.session.commit() # 注意仍然需要调用这一行来提交改动

#删除
>>> movie = Movie.query.get(1)
>>> db.session.delete(movie) # 使用 db.session.delete() 方法删除记录， 传入模型实例
>>> db.session.commit() # 提交改动
```

<br>

### 命令注册

参考：[Python 命令行之旅：深入 click 之选项篇](https://www.lagou.com/lgeduarticle/69961.html)

```python
@app.cli.command()  # 注册命令
@click.option('--drop', is_flag=True, help='create after drop')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
```

![image-20200415092634625](README.assets/image-20200415092634625.png)

<br>

<br>

## chapter06 模板的优化

自定义错误页面+模板的上下文处理函数+模板继承

### 自定义错误页面

```python
# 定义自定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404  # 这里是有两个返回值吗
```

<br>

### 模板的上下文处理函数

```python
# 上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
```

<br>

### 模板继承

```html
{% extends 'base.html' %}

{% block content %}
    <ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
            <a href="{{ url_for('index') }}">Go Back</a>
        </span>
    </li>
    </ul>
{% endblock %}
```

![image-20200419101337847](README.assets/image-20200419101337847.png)



<br>

<br>

## chapter 7 表单

表单的显现+表单的增删**改**。

其中最重要的是改。

### 显示

```python
    user = User.query.first()  # 读取第一个用户信息 --》用于base.html
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user, movies=movies)
```

<br>

### 删除

删除是最简单的操作。

```html
<!-- html中增加一个删除按钮，传递变量movie.id -->
 <a class="btn" href="{{url_for('edit',  movie_id=movie.id)}}">修改</a>
```

```python
# 查询删除
@app.route('/movie/delete/<int:movie_id>')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
```

<br>

### 增加

```html
<!-- index.html中增加一个表格 -->   
<form method="post">
    Name <input type="text" name="title" autocomplete="on" required>
    Year <input type="text" name="year" autocomplete="on" required>
    <input class="btn" type="submit" name="submit" value="Add">
</form>
```

```python
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
```

<br>

### 修改

**修改是表格中一个难点**。当时思考的时候，画了个图。懒得整理，就它吧。

![edit](README.assets/edit-1587310076178.jpg)

![image-20200419233011396](README.assets/image-20200419233011396.png)

<br>

<br>

## chapter8 用户认证

**使用 Flask-Login 实现用户认证**

不知道对不对：**login_user**（user）将用户信息存入session ---> **load_user**(user_id)根据用户信息的id,做相关的操作，最后将user对象赋给current_user这个全局对象 ---> **current_user.is_authenticated** 很轻松判断用户是否认证 ---》在html中根据是否认证**{% if current_user.is_authenticated %}**，给出不同的页面。

### 准备

login_manager = **LoginManager**(app) # 实例化扩展类

**load_user**返回的user对象赋给current_user这个全局对象。

继承**UserMixin**这个类会让 User 类拥有几个用于判断认证状态的属性和方法， 其中最常用的是 is_authenticated 属性： 如果当前用户已经登录， 那么**current_user.is_authenticated 会返回 True** ， 否则返回 False 。 有了
current_user 变量和这几个验证方法和属性， **我们可以很轻松的判断当前用户的认证状态**。

```python
from flask_login import LoginManager
login_manager = LoginManager(app) # 实例化扩展类

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数， 接受用户 ID 作为参数
	user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
	return user # 返回用户对象

from flask_login import UserMixin
class User(db.Model, UserMixin):
```

<br>

### 登录

用户的用户名密码验证通过之后，我们可以使用**login_user**（user）来使用户登录。`login_user()`方法会帮助你操作用户Session，并且会在请求上下文中记录用户信息。

```python
from flask_login import login_user

# 验证用户名和密码是否一致
if username == user.username and user.validate_password(assword):
    login_user(user) # 登入用户
    flash('Login success.')
	return redirect(url_for('index'))
```

<br>

### 登出

```python
# 登出
@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))
```

<br>

### 视图保护

```python
@login_required # 登录保护
if not current_user.is_authenticated: # 如果当前用户未认证
```

<br>

### 模板保护

```html
{% if current_user.is_authenticated %}
{% endif %}
```

![image-20200420225929291](README.assets/image-20200420225929291.png)

![image-20200420225957907](README.assets/image-20200420225957907.png)

<br>

<br>

## chapter 9 测试

> 在此之前， 每次为程序添加了新功能， 我们都要手动在浏览器里访问程序进行测
> 试。 除了测试新添加的功能， 你还要确保旧的功能依然正常工作。 在功能复杂的大
> 型程序里， 如果每次修改代码或添加新功能后手动测试所有功能， 那会产生很大的
> 工作量。 另一方面， 手动测试并不可靠， 重复进行测试操作也很枯燥。
> 基于这些原因， 为程序**编写自动化测试就变得非常重要**。

**测试客户端+测试命令**

app.test_client() 返回一个测试客户端对象， 可以用来模拟客户端（ 浏览器） ， 我们创建类属性 self.client 来保存它。 对它调用 get() 方法就相当于浏览器向服务器发送 GET 请求， 调用 post() 则相当于浏览器向服务器发送POST 请求， 以此类推。

除了测试程序的各个视图函数， 我们还需要测试自定义命令。 app.test_cli_runner() 方法返回一个命令运行器对象， 我们创建类属性self.runner 来保存它。 通过对它调用 invoke() 方法可以执行命令， 传入命令函数对象， 或是使用 args 关键字直接给出命令参数列表。 invoke() 方法返回的命令执行结果对象， 它的 output 属性返回命令的输出信息。

测试代码，我复制过来。

检测出3个错误。其他若干笔误。

![image-20200421175724159](README.assets/image-20200421175724159.png)

![image-20200421180225553](README.assets/image-20200421180225553.png)

如下所以，在html中，没有登录时候，不会有增加按钮等部分。

所以这行，没有必要测试。为了100%，我特地测试了这一行，这样覆盖率就100%，:smile:

![image-20200421181124272](README.assets/image-20200421181124272.png)

![image-20200421181100613](README.assets/image-20200421181100613.png)

<br>

<br>

## chapter09 使用包组织代码

如果，代码再大些，将是函数再分。用蓝图。

![image-20200421220011150](README.assets/image-20200421220011150.png)

<br>

<br>

## 附录

[生成 GitHub README.md 目录](https://sleepeatcode.com/articles/15/generating-the-github-readme-directory)

