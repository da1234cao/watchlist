from app import app
from flask import render_template
from app.models import User


# 定义自定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('errors/404.html'), 404  # 这里是有两个返回值吗
