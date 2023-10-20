from flask import Blueprint, render_template, request, redirect, g, url_for
from .forms import BookForm, TagForm
from models import BookModel,TagModel
from exts import db
from decorators import login_required
book = Blueprint("book", __name__, url_prefix = "/book")

@book.route('/index')
def index():
    books = BookModel.query.order_by(BookModel.publish_time.desc()).all()
    return render_template('book_staff/books.html',books=books)


# 注意路由映射要加载自定义装饰器之上
@book.route('/public',methods=['GET','POST'])
@login_required
def public():
    if request.method == 'GET':
        return render_template('book_staff/public.html')
    else:
        form = BookForm(request.form)
        # if form.validate() and g.user: # 判断条件加入g.user，因为在没有登录情况下无法发布，此处使用装饰器
        if form.validate():
            pass
            book = BookModel(
                bookname = form.bookname.data,
                author = form.author.data,
                publisher_id = g.user.id
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('book.index'))
        else:
            return redirect(url_for('book.public'))

@book.route('/info/<id>')
def info(id):
    book = BookModel.query.filter_by(id=id).first()
    return render_template('book_staff/info.html',book=book)

@book.post('/public/tag')
@login_required
def public_tag():
    form = TagForm(request.form)
    if form.validate():
        tag = TagModel(
            name=form.name.data,
            user_id=g.user.id,
            book_id=form.book_id.data
        )
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('book.info',id=form.book_id.data))
    else:
        print(form.errors)
        return redirect(url_for('book.info',id=request.form.get('book_id')))

@book.route('search')
def search():
    name = request.args.get('name')
    books = BookModel.query.filter(
        BookModel.bookname.contains(name)
    ).all()
    return render_template('book_staff/books.html',books=books)