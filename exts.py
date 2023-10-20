'''
ext.py 扩展文件

循环引用：
ImportError: cannot import name 'XXX' from partially initialized module 'XXX' (most likely due to a circular import)
db：app.py中的数据库对象
model：表抽象类

model创建需要继承自db.Model类(app.py)
app.py创建时同时需要引用model（因为如果不导入，数据库迁移的时候识别不到模型）

'''
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()