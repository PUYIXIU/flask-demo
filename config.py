# 主机名
HOSTNAME = "127.0.0.1"
# MySQL端口
PORT = 3306
# 用户名
USERNAME = 'root'
# 密码
PASSWORD = 'root123'
# 数据库名称
DATABASE = 'book_staff'
# 数据库链接url
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
'''
flask-mail 一个用于发送邮箱的python库
授权邮箱：设置
POP3/SMTP/IMAP 开启
邮箱绑定的手机号码发送验证短信到服务商
客户端授权码：EFRRUODWNRGSHQPO
'''
# 服务器地址
MAIL_SERVER = 'smtp.163.com'
# 使用SSL协议加密
MAIL_USE_SSL = True
# SSL端口号
MAIL_PORT = 465
# 邮箱账号
MAIL_USERNAME = "piuyixiu@163.com"
# 开启SMTP服务时生成的授权码
MAIL_PASSWORD = "EFRRUODWNRGSHQPO"
# 邮箱账号
MAIL_DEFAULT_SENDER = "piuyixiu@163.com"