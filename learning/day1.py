from flask import Flask, request, render_template
from datetime import datetime
# __name__:代表app.py模块
app = Flask(__name__)


# 1 创建路由和视图函数的映射
@app.route('/')
def hello_world():
    return '''
    <h1>Hello Flask</h1>
    '''


@app.route('/hello')
def hello():
    return 'hello'


# 2 带参数的url映射
@app.route('/user/<id>')
def user(id):
    return f"Welcome, user {id}"


# 3 限定参数类型的url映射
@app.route('/page/<int:page_num>')
def page(page_num):
    return f"page {page_num}"


# 4 默认参数的url映射
@app.route('/list/')
def list():
    page = request.args.get('page', 1)
    return f"list page： {page}"


# 5 渲染jinjia2模板
@app.route('/jinjia2')
def jinjia2():
    return render_template('index.html')


# 6 渲染jinjia2模板并传入参数
@app.route('/blog/<title>/<content>')
def blog(title, content):
    return render_template('blog.html', title=title, content=content)


class User:
    def __init__(self, **args):
        self.name = args["name"]
        self.email = args["email"]


# 7 渲染jinjia2模板传入类/可变类型参数
@app.route('/user-info')
def user_info():
    user = User(
        name=request.args.get("name", "default name"),
        email=request.args.get("email", "123456@default.com")
    )
    return render_template('user-info.html', user=user)

# 8 过滤器
def date_format(time, format='%Y-%m-%d'):
    return time.strftime(format)
app.add_template_filter(date_format,'dformat')  # 自定义过滤器

@app.route('/filter/<title>')
def filter(title):
    mytime = datetime.now()
    return render_template('filter.html', title=title, mytime=mytime)

# 9 控制语句
@app.route('/control/<age>')
def control(age):
    arr = [1,2,3]
    return render_template('control.html', age=int(age), arr=arr)

# 10 模板继承
@app.route('/child')
def child():
    return render_template('child.html')

# 11 加载静态资源
@app.route('/static')
def static_resource():
    return render_template('static.html')

'''
项目配置（重启有效）
1 debug模式 热更新模式
    edit configurations > FLASK_DEBUG = on
2 host
    edit configurations > Additional options = --host=0.0.0.0
3 port
    edit configurations > Additional options = --host=0.0.0.0 --port=8060
'''

'''
URL与视图的映射
url：http://127.0.0.1:5000/abc/
url一般由以下三部分构成：
1 协议 http/https
    http 默认端口 80
    https 默认端口 443
    在访问域名时，默认加上url使用协议的端口：
    baidu.com:443 (https://www.baidu.com)
2 ip/域名  
3 路由path
访问装饰器配置的路由时，会执行装饰器下方的函数，函数的返回值就是渲染内容
@app.route('/path')  # 路由配置
def path_mapping():  # 映射函数
    return '渲染内容' # 返回渲染内容

'''

if __name__ == '__main__':
    # app.run(debug=True)  # 同样开启debug功能
    app.run()
