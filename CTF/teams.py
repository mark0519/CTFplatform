from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort
from CTF.models import team,user
from CTF import login,db

bp = Blueprint('/teams', __name__)


@bp.route('/teams', methods=['GET','POST'])
def fteams():
    if not login.myself:
        return redirect('../auth/login')
    
    # 'tname=' + tname + '&tmessage=' + tmessage
    if request.method == 'POST':
        tname = request.form['tname']
        tmessage = request.form['tmessage']
        tname=str(tname)
        print(tname,tmessage)

        jg_name = team.query.filter(team.team_name == tname).first()
        if not jg_name:
            new = team(team_name = tname,team_capid = login.myself.user_id,team_intro = tmessage,team_score = 0,team_state = 1,team_sum=1)
            db.session.add(new)
            db.session.commit()
            myself = user.query.filter(user.user_id == login.myself.user_id).first()
            myself.user_teamid = team.query.filter(team.team_name == tname).first().team_id
            myself.is_captain =1
            db.session.add(myself)
            db.session.commit()
        else:                                       #队伍名称重复
            return jsonify({'code': 0}),200
    
    allteams=[]
    i = 1 
    t = None
    while 1:
        t = team.query.filter(team.team_id == i).first()
        if not t:
            break
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

    name = login.myself.user_name                #用户名信息
    if login.myself.user_teamid!=None:        #已经加入队伍
        teams = 1
        return render_template('teams/teams.html',allteams=allteams,name=name,teams=teams)
    return render_template('teams/teams.html',allteams=allteams,name=name)