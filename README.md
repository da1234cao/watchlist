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

#### 自定义错误页面

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

## 附录

[生成 GitHub README.md 目录](https://sleepeatcode.com/articles/15/generating-the-github-readme-directory)

