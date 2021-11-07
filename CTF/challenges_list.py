# -*- coding: utf-8 -*-=
from typing import ContextManager
from CTF import db,login
from CTF.models import que,user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/challenges_list', __name__)


@bp.route('/admin/challenges_list', methods=['GET','POST'])
def challenges_list():
    if not login.myself or login.myself.user_teamid !=1:
        return redirect('../auth/login')
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['cname']
        cate = request.form['category']
        value = request.form['value']
        state =request.form['state']
        flag = request.form['flag']
        mes = request.form['cmessage']
        name=str(name)
        cate=str(cate)
        flag=str(flag)

        print(id,'*',name,'*',cate,'*',value,'*',state,'*',flag,'*',mes)
        """
        'id='+id+'&cname=' + cname + '&category=' + category + '&value=' + value + '&state=' + state + '&flag='
         + flag + '&cmessage=' + cmessage
        """
        jg_name = que.query.filter(que.que_name == name).first()
        print(jg_name.que_id)
        print("******&&&&*****")
        print(id)
        if not jg_name or jg_name.que_id == int(id):                   # 若无重复题目名
            new = que.query.filter(que.que_id == id).first()
            new.que_name = str(name)
            new.que_cate = str(cate)
            new.que_score = value
            new.que_state = state
            new.que_flag = str(flag)
            new.que_intro = mes
            db.session.add(new)
            db.session.commit()
        else:                                   #题目名称重复！！
            return jsonify({'code': 0}),200
    else:
        pass

    
    challenges = []

    i = 1 
    q = None
    while 1:
        q = que.query.filter(que.que_id == i).first()
        if not q:
            break

        """
        database需要的参数如下:
        """
        challenges.append({
        'id': q.que_id,
        'name': q.que_name,
        'cate': q.que_cate,
        'value': q.que_score,
        'state': q.que_state,    #1为显示
        'flag': q.que_flag,
        'message': q.que_intro,
        })
        i += 1

    name = login.myself.user_name                #用户名信息
    return render_template('admin/challenges_list.html', challenges=challenges,name=name)
