# -*- coding: utf-8 -*-=
import os
from flask.scaffold import F

from werkzeug.utils import secure_filename

from CTF import db
from CTF.models import que
new_que_id=0

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/new', __name__)


@bp.route('/admin/new', methods=['GET', 'POST'])
def challenges_list():
    global new_que_id
    if request.method == 'POST':
        cname = request.form.get('cname')
        category = request.form.get('category')
        value = request.form.get('value')
        state = bool(request.form.get('state'))
        flag = request.form.get('flag')
        cmessage = request.form.get('cmessage')


        '''
        cname 题目名字(字符串)
        category 题目类型(字符串)
        value 题目分值(int)
        state 题目是否隐藏(bool 1代表显示,0代表隐藏)
        flag 题目flag(字符串)
        cmessage 题目详情(长字符串)
        id (题目唯一id,从数据库拿出最大的id然后+1赋值给他)
        上传的文件路径都在 CTFplatform/upload/ 目录下
        '''
        
        print("cname==>", cname)
        print("cmessage==>", cmessage)

        new_que = que(cname,category,flag,cmessage,state,value)
        new_que.que_nowscore=value
        db.session.add(new_que)
        db.session.commit()
        new_que_id = que.query.filter(que.que_name == cname).first().que_id
        print(new_que_id)

        return render_template('admin/new.html')
    else:
        return render_template('admin/new.html')
