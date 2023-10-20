from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(200), nullable=False, unique=True)  # unique 值唯一
    # default=函数名（注意不是函数调用）第一次调用时调用此函数
    join_time = db.Column(db.DateTime, default=datetime.now)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(200), nullable=True)

# book model
class BookModel(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publish_time = db.Column(db.DateTime, default=datetime.now)
    bookname = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    publisher = db.relationship(UserModel, backref="book")

class TagModel(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(UserModel, backref="tags")
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    # BookModel中反向收集的tag根据tag创建的时间排序
    book = db.relationship(
        BookModel,
        backref=db.backref("tags", order_by=create_time.desc())
    )