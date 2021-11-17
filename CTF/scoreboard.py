from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from sqlalchemy.sql import func
from CTF import db
from CTF.models import user,team,que

def takeSecond(elem):
    return elem[1]
bp = Blueprint('scoreboard', __name__)


@bp.route('/scoreboard')
def index():
    if 'id' not in session:
        return redirect('../auth/login')

    list=[]
    team_id = db.session.query(func.max(team.team_id)).scalar()
    i = 1 
    t = None
    while i <= team_id:
        t = team.query.filter(team.team_id == i).first()
        if not t:
            i+=1
            continue
        if t.team_state == 0:
            i+=1
            continue 
        list.append([t.team_name,t.team_score]) # 战队总分
        i += 1
    list.sort(key=takeSecond,reverse=True)
    teams = []
    for i in range(len(list)):
        teams.append({
            'place': i+1,
            'name' :list[i][0],
            'score':list[i][1]
        })
    
    i = 1
    u = None
    list = []
    while 1:
        u = user.query.filter(user.user_id == i).first()
        if not u:
            break
        if u.user_state == 0:
            i+=1
            continue

        list.append([u.user_name,u.user_score])
        i += 1
    users = []
    list.sort(key=takeSecond,reverse=True)
    for i in range(len(list)):
        users.append({
            'place': i+1,
            'name' :list[i][0],
            'score':list[i][1]
        })

    i = 1
    num = 0
    web=pwn=re=misc=cry=0
    q = None
    while 1:
        q = que.query.filter(que.que_id == i).first()
        if not q:
            break
        if q.que_state == 0:
            i+=1
            continue
        if str(q.que_cate) == 'Web':
            web+=1
        if str(q.que_cate) == 'Pwn':
            pwn+=1
        if str(q.que_cate) == 'Re':
            re+=1
        if str(q.que_cate) == 'Misc':
            misc+=1
        if str(q.que_cate) == 'Crypto':
            cry+=1
        i += 1
        num += 1
    # print(num)
    if num == 0:
        web = pwn = re = misc = cry = 0
    else:
        web = web/num*100 
        pwn = pwn/num*100
        re = re/num*100
        misc = misc/num*100
        cry = cry/num*100
    # print(web,pwn,re,misc,cry)
    name = session.get('username')
    return render_template('scoreboard/scoreboard.html' ,users=users ,teams=teams ,web=web,pwn=pwn,re=re,misc=misc,cry=cry,name=name)
