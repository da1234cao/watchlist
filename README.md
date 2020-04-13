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

