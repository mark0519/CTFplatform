# -*- coding: utf-8 -*-=
import os

from werkzeug.utils import secure_filename

from CTF import db,new
from CTF.models import que
import uuid

def random_filename(filename):  #上传文件重命名
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/new_file', __name__)


@bp.route('/admin/new_file', methods=['POST'])
def challenges_list():

    print("*********new_file")
    if request.method == 'POST':
        file = request.files['file']
        print(request.files)
        filename=random_filename(file.filename)
        file.save(os.path.join('upload/', secure_filename(filename)))

        path = 'CTFplatform/CTF/upload/'+str(filename)
        print(new.new_que_id)
        new_que = que.query.filter(que.que_id == new.new_que_id).first()
        new_que.que_address=path
        db.session.add(new_que)
        db.session.commit()

    return redirect('challenges_list')
