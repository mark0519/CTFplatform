# -*- coding: utf-8 -*-=
import os
from flask.scaffold import F
from sqlalchemy.sql import func

from werkzeug.utils import secure_filename

from CTF import db,login
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
    if not login.myself or login.myself.user_teamid !=1:
        return redirect('../auth/login')
    if request.method == 'POST':
        cname = request.form.get('cname')
        category = request.form.get('category')
        value = request.form.get('value')
        state = bool(request.form.get('state'))
        flag = request.form.get('flag')
        cmessage = request.form.get('cmessage')

        cname=str(cname)
        category=str(category)
        flag=str(flag)
        if not que.query.filter(que.que_id == 1).first():
            new_que_id = 0
        else:   
            new_que_id = db.session.query(func.max(que.que_id)).scalar()
            print("NEW_QUE_ID:")
            print(new_que_id)
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
        jg_name = que.query.filter(que.que_name == cname).first()
        if not jg_name:  # 若无重复题目名
            new_que = que(cname,category,flag,cmessage,state,value)
            new_que.que_score=value
            new_que_id+=1
            new_que.que_id = new_que_id
            db.session.add(new_que)
            db.session.commit()
            print(new_que_id)
        else:                                                   #题目名字重复
            return jsonify({'code': 0}),200

        name = login.myself.user_name
        return render_template('admin/new.html',name=name)
    else:
        name = login.myself.user_name
        return render_template('admin/new.html',name=name)
