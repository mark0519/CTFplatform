from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify,session
)
from werkzeug.exceptions import abort
from sqlalchemy.sql import func

from CTF.models import team,user
from CTF import db

new_team_id = 1
bp = Blueprint('/teams', __name__)


@bp.route('/teams', methods=['GET','POST'])
def fteams():
    global new_team_id
    if 'id' not in session:
        return redirect('../auth/login')

    # 'tname=' + tname + '&tmessage=' + tmessage
    if request.method == 'POST':
        tname = request.form['tname']
        tmessage = request.form['tmessage']
        tname=str(tname)
        print(tname,tmessage)
        if not tname:                               #队名为空
            return jsonify({'code': -1}),200
        myself = user.query.filter(user.user_id == session.get('id')).first()

        if myself.user_teamid!=None:                #有队伍或正在申请
            return jsonify({'code': -2}),200

        new_team_id = db.session.query(func.max(team.team_id)).scalar()
        jg_name = team.query.filter(team.team_name == tname).first()
        if not jg_name:
            new_team_id += 1 
            team_id = new_team_id
            new = team(team_id = team_id,team_name = tname,team_capid = session.get('id'),team_intro = tmessage,team_score = myself.user_score,team_state = 1,team_sum=1)
            for i in myself.user_ans:
                new.team_ans.append(i)
            db.session.add(new)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            myself.user_teamid = team.query.filter(team.team_name == tname).first().team_id
            myself.is_captain =1
            db.session.add(myself)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
        else:                                       #队伍名称重复
            return jsonify({'code': 0}),200

    new_team_id = db.session.query(func.max(team.team_id)).scalar()
    allteams=[]
    i = 1 
    t = None
    while i <= new_team_id:
        t = team.query.filter(team.team_id == i).first()
        if not t:
            i+=1
            continue
        if t.team_state == 0:
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

    name = session.get('username')       #用户名信息
    me = user.query.filter(user.user_id==session.get('id')).first()
    if me.user_teamid!=None and (me.is_captain==0 or me.is_captain==1):        #已经加入队伍
        teams = 1
        return render_template('teams/teams.html',allteams=allteams,name=name,teams=teams)
    return render_template('teams/teams.html',allteams=allteams,name=name)