import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db
'''
flask-wtf 验证数据格式
是wtforms对flask的封装
wtforms.Form主要用于验证前端提交的数据是否符合要求
'''
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Please check email form')])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="captcha is not correct")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='Please check username form')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Please check password form')])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 验证邮箱是否被注册过
    def validate_email(self, field):
        print(field.data)
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="email already being registered")

    # 检查验证码是否正确
    def validate_captcha(self, field):
        code = field.data
        email = self.email.data
        code_model = EmailCaptchaModel.query.filter_by(code=code,email=email).first()
        if not code_model:
            raise wtforms.ValidationError(message="code is not correct")
        else:
            db.session.delete(code_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Please check your email")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="Please check your password")])

class BookForm(wtforms.Form):
    bookname = wtforms.StringField(validators=[Length(min=1,max=20,message="Please check book name")])
    author = wtforms.StringField(validators=[Length(min=1,max=20,message="Pleas check author name")])

class TagForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=1,max=10,message='illegal tag name')])
    book_id = wtforms.IntegerField(validators=[InputRequired(message="you must pick a book")])
