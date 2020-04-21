import click
from app import app, db
from app.models import User, Movie


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
