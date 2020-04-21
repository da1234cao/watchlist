import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库的连接配置放在.env文件中。
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('mysql_connect')
db = SQLAlchemy(app)  # 初始化扩展， 传入程序实例 app

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'dev'


# 回调函数
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    user = User.query.get(int(user_id))
    return user


# 上下文处理函数
@app.context_processor
def inject_user():
    from app.models import User
    user = User.query.first()
    return dict(user=user)


# 导入这些模块，相当于在这里展开
from app import views, errors, commands, models
