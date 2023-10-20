from functools import wraps
from flask import g, redirect, url_for
'''
装饰器实际上是对函数的包装

装饰器使用方法
@my_decorator
def anying_function():

装饰器定义方法 
def my_decorator(func):  # func即装饰器下方作用的函数
    @wraps(func) 保留函数信息
    def inner(): # inner是对func的一种包装
        pass
    return inner # 最终实际调用的是inner
'''

def login_required(func):
    # 保留func的信息
    @wraps(func)
    # inner的参数就是func被调用时传入的参数
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('book.index'))
    return inner
