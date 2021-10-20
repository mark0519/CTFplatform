from CTF import db
from CTF.models import user

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import hashlib

bp = Blueprint('/auth/register', __name__)


@bp.route('/auth/register', methods=['GET', 'POST'])
def index():

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

        jg_name = user.query.filter(user.user_name == username).first()
        
        if not jg_name:  # 若无重复用户名
            new_user = user(username,email,password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'code': 1, 'msg': 'pass'})
        else:  # 若有重复用户名
            print('code == 0')
            return jsonify({'code': 0, 'msg': 'error'})

    return render_template('auth/register/register.html')
