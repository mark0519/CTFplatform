# -*- coding: utf-8 -*-=
import time
from CTF import login
from CTF.models import user,que,db,team

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,session
)
from werkzeug.exceptions import abort

bp = Blueprint('/users', __name__)


@bp.route('/users', methods=['GET', 'POST'])
def aaaaa():
    if 'id' not in session:
        return redirect('../auth/login')
    if request.method == 'POST':
        logout = request.form['logout']
        print(type(logout))
        if logout=='1':
            session.clear()
            return redirect('../auth/login')
        oldpassword = request.form['oldpasswd']
        newpassword = request.form['newpasswd']
        print(oldpassword)
        print(newpassword)

        md5 = hashlib.md5()
        md5.update(oldpassword.encode('utf-8'))
        oldpassword = md5.hexdigest()
        print(oldpassword)
        md5 = hashlib.md5()
        md5.update(newpassword.encode('utf-8'))
        newpassword = md5.hexdigest()
        print(newpassword)

        myself = user.query.filter(user.user_id==session.get('id')).first()
        if oldpassword == myself.user_pwd:
            myself.user_pwd = newpassword
            db.session.add(myself)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return jsonify({'code': 1})
        else:
            print("旧密码错误")
            return jsonify({'code': 0})
    else:
        pass

    me = user.query.filter(user.user_id==session.get('id')).first()
    t = team.query.filter(team.team_id == me.user_teamid).first()
    if not t:
        t = 'no team'
    else:
        t = t.team_name

    username=me.user_name
    score=me.user_score
    email=me.user_mail

    challenges=[]
    i = 1 
    q = None
    while 1:
        q = que.query.filter(que.que_id == i).first()
        if not q:
            break
        myself_ans = user.query.filter(user.user_ans.any(que.que_id == q.que_id)).first()
        if not myself_ans:
            i+=1
            continue
        """
        database需要的参数如下:
        """
        challenges.append({
        'name': q.que_name,
        'cate': q.que_cate,
        'score':q.que_score
        })
        i+=1
        print("****x")


    name = session.get('username')               #用户名信息
    return render_template('users/users.html',challenges=challenges,username=username,score=score,email=email,name=name,team=t)
