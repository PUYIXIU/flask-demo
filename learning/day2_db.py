import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

os.environ["FLASK_ENV"] = 'development'
os.environ["FLASK_DEBUG"] = '1'

app = Flask(__name__)
app.debug = True
# 1 在app.config中配置好数据库信息
# 主机名
HOSTNAME = "127.0.0.1"
# MySQL端口
PORT = 3306
# 用户名
USERNAME = 'root'
# 密码
PASSWORD = 'root123'
# 数据库名称
DATABASE = 'books'

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# 2 使用SQLAlchemy(app)创建一个db对象
db = SQLAlchemy(app)
migrate = Migrate(app, db)

## Migrate ORM模型映射成表的三步：
### 1 flask db init 初始化数据库，仅执行一次
### 2 flask db migrate 识别ORM模型的改变，生成迁移脚本（migrations/versions下的迁移脚本）
### 3 flask db upgrade 运行迁移脚本
# 3 SQLAlchemy会自动读取app.config中连接db的信息
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text('select 1'))
#         print(rs.fetchone())

'''
ORM 模型
Object Relationship Map
'''
class Book(db.Model):  # 需继承自db.Model
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id")) # 作者id 关联到Author库
    # 通过author_id 从Author库中将对应author信息拉取过来
    # back_populates 反向聚集，表示从找到author_id对应的author下的所有book
    # author_info = db.relationship("Author", back_populates="book")
    # 使用backref就无需手动在反向聚集的类中添加聚集关联属性了
    author_info = db.relationship("Author", backref="book")

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.Date)
    # book = db.relationship("Book", back_populates="author_info")

# db.create_all 浅更新表
# with app.app_context():
#     db.create_all()  # 创建所有表格


'''
增
add
commit
'''
@app.route('/add_book')
def add_book():
    try:
        name = request.args.get("name")
        author = request.args.get("author")
    except:
        return 'params error！'
    book = Book(name=name, author_id=author)
    db.session.add(book)
    db.session.commit()
    return 'add success'

'''
查
Obj.query 是继承自db.Model的属性
get(primary_key) 通过主键查询
filter_by(key=value,...)    返回QuerySet
    filter_by()[0] 和 filter_by().first()的区别：
        前者查询为空时会报错，后者不会报错
'''
@app.route('/get_book/<id>')
def get_book(id):
    book = Book.query.get(int(id))
    if(book):
        print(book.author_info.book)
        return f'''
            作者名称：{book.author_info.name}\n
            作者国籍：{book.author_info.country}\n
            作者其他作品：{",".join([i.name for i in book.author_info.book])}\n
        '''
    else:
        return "no data"

@app.route('/query_book/<name>')
def query_book(name):
    book = Book.query.filter_by(name=name)
    result = ''
    for i  in book:
        result+=f"<li>{i.name} ——{i.author_id}</li>"
    return result

# 改
@app.route("/update_book/")
def update_book():
    try:
        id = request.args.get("id")
        name = request.args.get("name")
    except:
        return "params error"
    if not id or not name: return 'params error'
    book = Book.query.get(id)
    if book:
        book.name = name
        db.session.commit()
        return 'update success'
    else:
        return 'no data'

# 删
@app.route('/delete_book/<id>')
def delete_book(id):
    book = Book.query.get(id)
    if not book: return 'no data'
    db.session.delete(book)
    db.session.commit()
    return 'delete success'

@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    app.run()