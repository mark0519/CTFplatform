from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from CTF import login     
from CTF.models import user

bp = Blueprint('home', __name__)


@bp.route('/')
def index():

    if 'id' in session:
        is_admin = 0
        if user.query.filter(user.user_id == session.get('id')).first().user_teamid == 1:            #1表示是管理员
            is_admin = 1
        name = session.get('username')          #用户名信息
        return render_template('home/home.html', name=name , is_admin=is_admin)
    # print(session)
    # print("*********")
    return render_template('home/home.html')




