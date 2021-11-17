from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session,jsonify
)
from werkzeug.exceptions import abort
from CTF.models import user,team
from sqlalchemy.sql import func
from CTF import db

bp = Blueprint('/admin/edit_teams', __name__)


@bp.route('/admin/edit_teams', methods=['GET','POST'])
def feteams():
    if 'id' not in session or user.query.filter(user.user_id == session.get('id')).first().user_teamid !=1:
        return redirect('../auth/login')

    if request.method == 'POST':
        '''
        cmd == 0 ==> 啥也不是
        cmd == 1 ==> 解散战队[id]
        cmd == 2 ==> 隐藏战队[id]
        cmd == 3 ==> 显示战队[id]
        '''
        id = request.form['id']
        cmd = request.form['cmd']
        id = int(id)
        cmd = int(cmd)
        print(id,cmd)
        if cmd == 1:
            oldteam = team.query.filter(team.team_id == id).first()
            id = oldteam.team_capid
            db.session.delete(oldteam)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            u = user.query.filter(user.user_id== id).first()
            u.is_captain = 0
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()               
            return jsonify['code': 1],200
        if cmd == 2:
            oldteam = team.query.filter(team.team_id == id).first()
            oldteam.team_state = 0
            db.session.add(oldteam)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return jsonify['code': 1],200
        if cmd == 3:
            oldteam = team.query.filter(team.team_id == id).first()
            oldteam.team_state = 1
            db.session.add(oldteam)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return jsonify['code': 1],200

    allteams=[]
    team_id = db.session.query(func.max(team.team_id)).scalar()
    allteams=[]
    i = 1 
    t = None
    while i <= team_id:
        t = team.query.filter(team.team_id == i).first()
        if not t:
            i+=1
            continue

        captain = user.query.filter(user.user_id == t.team_capid).first().user_name
        allteams.append({
        'id': t.team_id,
        'name': t.team_name,
        'captain': captain,
        'score': t.team_score, # 战队总分
        'sum': t.team_sum, # 战队人数
        'state': t.team_state
        })
        i += 1

    name = session.get('username')               #用户名信息
    return render_template('admin/edit_teams.html',name=name ,allteams=allteams)