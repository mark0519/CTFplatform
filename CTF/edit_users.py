from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort
from CTF import login,db
from CTF.models import user

bp = Blueprint('/admin/edit_users', __name__)


@bp.route('/admin/edit_users', methods=['GET','POST'])
def feusers():
    if not login.myself or login.myself.user_teamid !=1:
        return redirect('../auth/login')
    # 'id='+{{u.id}}+'&name=' + name + '&score=' + score + '&state=' + state
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        score = request.form['score'] # 总分
        state = request.form['state']
        name = str(name)
        print(id,name,score,state)

        jg_name = user.query.filter(user.user_name == name).first()
        
        new = user.query.filter(user.user_id == id).first()
        if not jg_name or jg_name == new:  # 若无重复用户名
            new.user_name = str(name)
            new.user_state = state
            new.que_score = score
            print("********1")
            db.session.add(new)
            print("********2")
            db.session.commit()
            print("********3")
        else:           #用户名重复不可更改
            return jsonify({'code': 0}),200

    users=[]
    i = 1 
    u = None
    while 1:
        u = user.query.filter(user.user_id == i).first()
        if not u:
            break

        """
        database需要的参数如下:
        """
        users.append({
        'id': u.user_id,
        'name': u.user_name,
        'score': u.user_score,
        'state': u.user_state,    #1为显示
        })
        i += 1

    name = login.myself.user_name
    return render_template('admin/edit_users.html',users=users,name=name)