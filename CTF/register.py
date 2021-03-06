from CTF import db
from CTF.models import user

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,session
)
from werkzeug.exceptions import abort
import hashlib

bp = Blueprint('/auth/register', __name__)


@bp.route('/auth/register', methods=['GET', 'POST'])
def index():
    if 'id' in session:
        return redirect('../../')
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['passwd']
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()

        username = str(username)
        email = str(email)
        print("username == " + username)
        print("email == " + email)
        print("password_md5 == " + password)

        if not email or not username or not password:
            return jsonify({'code': -1}),200                        #用户名或密码或邮箱为空



        '''
        email 是用户的邮箱
        username 是用户名
        password 是密码的md5值
        '''

        jg_name = user.query.filter(user.user_name == username).first()

        if not jg_name:  # 若无重复用户名
            new_user = user(username,email,password,None,0,1,0)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            print("code == 1 ")
            return jsonify({'code': 1, 'msg': 'pass'})
        else:  # 若有重复用户名
            print('code == 0')
            return jsonify({'code': 0, 'msg': 'error'})

    return render_template('auth/register/register.html')
