# -*- coding: utf-8 -*-=
import os

from werkzeug.utils import secure_filename

from CTF import db,new,login
from CTF.models import que,user
import uuid

def random_filename(filename):  #上传文件重命名
    ext = os.path.splitext(filename)[1]
    print(type(ext))
    print(ext)
    if ext =='.rar' or ext == '.7z'or ext =='.zip'or ext =='.tar'or ext =='.tar.gz':
        new_filename = uuid.uuid4().hex + ext
        return new_filename
    else:
        return None


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,session
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/new_file', __name__)


@bp.route('/admin/new_file', methods=['POST'])
def challenges_list():
    if 'id' not in session or user.query.filter(user.user_id == session.get('id')).first().user_teamid !=1:
        return redirect('../auth/login')

    if request.method == 'POST':
        file = request.files['file']
        print(request.files)

        if not file:
            new_que = que.query.filter(que.que_id == new.new_que_id).first()
            new_que.que_address=None
            db.session.add(new_que)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return redirect('challenges_list')
        filename=random_filename(file.filename)
        if not que.query.filter(que.que_id == new.new_que_id).first():           #题目名重复
            return jsonify({'code': 0}),200
        elif not filename:                            #文件类型出错
            q = que.query.filter(que.que_id == new.new_que_id).first()
            new.new_que_id -= 1
            db.session.delete(q)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return '''
            <script>
                alert("请上传压缩包格式文件");
                window.location.href="/admin/new";
            </script>
            '''
        else:
            file.save(os.path.join('CTF/upload', secure_filename(filename)))
            path = '/upload/'+str(filename)
            print(new.new_que_id)
            new_que = que.query.filter(que.que_id == new.new_que_id).first()
            new_que.que_address=path
            db.session.add(new_que)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
    
    return redirect('challenges_list')