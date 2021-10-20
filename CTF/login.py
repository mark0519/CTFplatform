# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/auth/login', __name__)


@bp.route('/auth/login', methods=['GET', 'POST'])
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    # 如果接收到数据
    if request.method == 'POST':
        account = request.form['name']
        password = request.form['passwd']
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()

        if '@' in account:
            email = account
            mode = 0
            print("Email == "+str(email))
        else:
            username = account
            mode = 1
            print("Username == "+str(username))
        print("mode == "+str(mode))
        print("password_md5 == " + password)
        '''
        mode = 0 是邮箱(email)登陆 
        mode = 1 是用户名(username)登陆
        email 是用户的邮箱
        username 是用户名
        使用其中一种方式登陆时另一个参数为空
        password 是密码的md5值
        '''

        if mode==0: 
            test = user.query.filter(user.user_mail == email).first()
            print("*****")
            if not test or test.user_pwd!=password:
                print('code == 0')
                return jsonify({'code': 0, 'msg': 'error'})
            else:
                print("code == 1")
                return jsonify({'code': 1, 'msg': 'pass'})
        if mode==1:
            test = user.query.filter(user.user_name == username).first()
            if not test or test.user_pwd!=password:
                print('code == 0')
                return jsonify({'code': 0, 'msg': 'error'})
            else:
                print("code == 1")
                return jsonify({'code': 1, 'msg': 'pass'})

    return render_template('auth/login/login.html')

