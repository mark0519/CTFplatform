# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import user

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






    else:
        pass

    database = ""
    '''
    上面那行' database = "" '是我方便调试写的,要和数据库数据对接的,需要的参数如下代码:
    '''
    challenges = [{
        'id': 0,
        'name': "test_challenges",
        'cate': "PWN",
        'value': 100,
        'state': 0,
        'flag': "flag{This_is_a_fake_flag}",
    }]

    for i in database:
        """
        database需要的参数如下:
        """
        challenges.append({
        'id': i.id,
        'name': i.name,
        'cate': i.cate,
        'value': i.value,
        'state': i.state,
        'flag': i.flag,
        })
    return render_template('admin/challenges_list.html', challenges=challenges)
