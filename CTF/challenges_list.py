# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import que

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/challenges_list', __name__)


@bp.route('/admin/challenges_list', methods=['GET','POST'])
def challenges_list():
    if request.method == 'POST':
        id = request.form['id']
        new_state = request.form['new_state']
        """
        前端传来的数据:id,new_state
        把数据库里id=id的题目的state状态改为new_state就行
        就在这个if里面完成数据库state的更改
        """
        new = que.query.filter(que.que_id == id).first()
        new.que_state = new_state
        db.session.add(new)
        db.session.commit()

    else:
        pass

    
    challenges = [{
        'id': 0,
        'name': "test_challenges",
        'cate': "PWN",
        'value': 100,
        'state': 0,
        'flag': "flag{This_is_a_fake_flag}",
    }]

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
        'state': q.que_state,    #1为隐藏
        'flag': q.que_flag,
        })
        i += 1

        print(challenges)
        print(q.que_flag+'*****')
        print("************")
    return render_template('admin/challenges_list.html', challenges=challenges)
