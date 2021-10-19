from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import hashlib

bp = Blueprint('/auth/register', __name__)


@bp.route('/auth/register', methods=['GET', 'POST'])
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['passwd']
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()

        print("username == " + username)
        print("email == " + email)
        print("password_md5 == " + password)
        '''
        email 是用户的邮箱
        username 是用户名
        password 是密码的md5值
        '''

        """
        待完善.....
        """

        if True:  # 如果没有数据异常,数据库填入正确
            print("code == 1")
            return jsonify({'code': 1, 'msg': 'pass'})
        elif False:  # 密码错误或者找不到用户account(用户名或密码错误)
            print('code == 0')
            return jsonify({'code': 0, 'msg': 'error'})

    return render_template('auth/register/register.html')
