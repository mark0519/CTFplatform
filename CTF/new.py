# -*- coding: utf-8 -*-=
import os

from werkzeug.utils import secure_filename

from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,
)
from werkzeug.exceptions import abort



bp = Blueprint('/admin/new', __name__)


@bp.route('/admin/new', methods=['GET', 'POST'])
def challenges_list():
    if request.method == 'POST':
        file = request.files['file']
        print(request.files)
        file.save(os.path.join('upload/', secure_filename(file.filename)))

        cname = request.form['cname']
        category = request.form['category']
        value = request.form['value']
        state = request.form['state']
        flag = request.form['flag']
        cmessage = request.form['cmessage']

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



        """
        
        """
        if True: # 一切正常
            return render_template('admin/challenges_list.html')
        else:
            return render_template('admin/new.html')
    else:
        return render_template('admin/new.html')

