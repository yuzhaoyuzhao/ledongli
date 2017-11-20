# -*- coding:utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


app = Flask(__name__)

#  设置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test'

# 设置自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SECRET_KEY'] = 's'

# 实例化 SQLAlchemy对象
db = SQLAlchemy(app)


# 创建表格单类,用于添加信息
class Append(FlaskForm):
    au_info = StringField(validators=[DataRequired()])
    bk_info = StringField(validators=[DataRequired()])
    submit = SubmitField(u'添加')


# 写接口
@app.route('/', methods=['GET', 'POST'])
def index():
    # 查询所有作者和图书信息
    au_list = Author.query.all()  # 是[对象, 对象, 对象]
    bo_list = Book.query.all()

    # 创建表单对象
    form = Append()
    if form.validate_on_submit():
        wtf_au = form.au_info.data
        wtf_bk = form.bk_info.data

        # 把表单数据存入模型类
        db_au = Author(name=wtf_au)
        db_bk = Book(info=wtf_bk)

        # 提交数据库会话
        db.session.add_all([db_au, db_bk])
        db.session.commit()

        # 添加数据后,再次查询
        author = Author.query.all()
        book = Book.query.all()


        return render_template('index.html', author=author, book=book, form=form)
    else:
        print('---------------------')
        print (au_list)
        print (bo_list)
        print('---------------------')
        return render_template('index.html', author=au_list, book=bo_list, form=form)


# 删除作者
@app.route('/delete_author<id>')
def delete_author(id):
    # 精确查询需要删除的作者id
    au = Author.query.get(id)
    db.session.delete(au)
    return redirect(url_for('index'))  # 返回首页


# 删除书的名字
@app.route('/delete_book<id>')
def delete_book(id):
    bk = Book.query.get(id)
    db.session.delete(bk)
    return redirect(url_for('index'))  # 返回首页


# 定义模型类---作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64))
    au_book = db.relationship('Book', backref='author')

    def __str__(self):
        return 'Author: %s, %s' % (self.name, self.email)


# 定义模型类---书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(32), unique=True)
    leader = db.Column(db.String(32))
    au_book = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __str__(self):
        return 'Book:%s, %s' % (self.info, self.leader)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au_xi = Author(name='我爱吃西红柿', email='xihongshi1@163.com')
    au_qian = Author(name='萧潜', email='xq@163.com')
    au_san = Author(name='唐家三少', email='sanshao@163.com')

    bk_xi = Book(info='吞噬星空', leader='罗峰')
    bk_xi2 = Book(info='寸芒', leader='李阳')
    bk_qian = Book(info='缥缈之旅', leader='李强')
    bk_san = Book(info='冰火魔橱', leader='融念冰')

    db.session.add_all([au_qian,au_san,au_xi,bk_qian,bk_san,bk_xi,bk_xi2])
    db.session.commit()

    app.run(debug=True)































