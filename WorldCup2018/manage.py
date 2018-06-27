# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 下午6:21
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : manage.py
# @Software: PyCharm

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run import create_app
from exts import db

app = create_app()
# 实例
manager = Manager(app)
# 绑定
Migrate(app, db)
# 添加命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    '''数据库'''
    # 初始化迁移环境:python3 manage.py db init
    # 迁移数据库:python3 manage.py db migrate
    # 映射数据库:python3 manage.py db upgrade
