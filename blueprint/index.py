# -*- codeing =utf-8 -*-
# @Time ： 2023/10/14 19:31
# @Author: wsy
# @File:index.py
# @Software: PyCharm

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, g
from models import EmailCaptchaModel, UserModel
from exts import mail,db
from flask_mail import Message
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
import string
import random

index = Blueprint("index",__name__, url_prefix="/index")

@index.route("/")
def home():
    return render_template('book_staff/index.html')

@index.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('book_staff/register.html')
    else:
        # 用户提交注册信息
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = generate_password_hash(form.password.data)
            user = UserModel(email=email,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index.login'))
        else:
            return redirect(url_for('index.register'))

@index.route('/mail/test')
def mail_test():
    message = Message(
        subject="邮箱测试",
        recipients=["1597167270@qq.com"],
        body="测试邮件"
    )
    mail.send(message)
    return '邮件发送成功！'

# url默认是GET请求
@index.route('/captcha/email', methods=['GET'])
def get_email_captcha():

    email = request.args.get('email')
    # string.digits =  '0123456789'
    source = string.digits*4
    # random.sample 随机取样
    captcha = "".join(random.sample(source, 4))
    message = Message(
        subject="your hot sweat verification code！",
        recipients=["1597167270@qq.com"],
        body=f"your code: {captcha}"
    )
    # memcached 缓存/redis/数据库
    mail.send(message)
    email_captcha = EmailCaptchaModel(
        email = email,
        code = captcha
    )
    db.session.add(email_captcha)
    db.session.commit()
    print('验证码发送成功')
    '''
    返回数据 需要满足 RESTful API的格式
    code message data
    '''
    return jsonify({
        'code':200,
        'message':'send success',
        'data': None
    })

@index.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('book_staff/login.html')
    else:
        form = LoginForm(request.form)
        if(form.validate()):
            email = form.email.data
            password = form.password.data
            user_model = UserModel.query.filter_by(email=email).first()
            if not user_model:
                return redirect(url_for('index.login'))
            else:
                if check_password_hash(user_model.password, password):
                    pass
                    '''
                    cookie session
                        一般用于存储少量的数据，如登录授权的东西
                        flask中的session是经过加密存储在cookie中的
                        session为一次会话中用于身份识别的
                    '''
                    session['user_id'] = user_model.id
                    return redirect("/")
                else:
                    return redirect(url_for('index.login'))
        else:
            return redirect(url_for('index.login'))

@index.route('/logout')
def logout():
    session.clear()
    del g.user
    return redirect('/')