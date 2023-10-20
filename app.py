import os
import config
from flask import Flask, session, g
from exts import db, mail
from flask_migrate import Migrate
# 从模型中导入orm模型
from models import UserModel, EmailCaptchaModel, BookModel

# 从蓝图中引入界面
from blueprint.index import index
from blueprint.book import book

os.environ['FLASK_ENV'] = 'development'
os.environ["FLASK_DEBUG"] = '1'

app = Flask(__name__)
app.secret_key = 'supper_secret'
app.config.from_object(config)

db.init_app(app)  # 数据库
mail.init_app(app)  # 邮箱

migrate = Migrate(app, db)

app.register_blueprint(index)
app.register_blueprint(book)

# 钩子函数 hook
# before_request 请求之前
# before_first_request 首次请求之前
# after_request 请求之后


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.filter_by(id=user_id).first()
        setattr(g, "user", user)
    else:
        setattr(g, 'user', None)
    pass

# @app.after_request
# def my_after_request():
#     pass

# 上下文处理器 存放在一些模板中公用的属性
@app.context_processor
def my_context_processor():
    return {"user":g.user}

@app.route('/')
def hello():
    return 'hello'

if(__name__ == '__main__'):
    app.run()

