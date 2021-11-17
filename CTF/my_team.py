from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,session
)
from werkzeug.exceptions import abort
from CTF.models import team, user,que
from CTF import teams, db

bp = Blueprint('/my_team', __name__)


@bp.route('/my_team', methods=['GET', 'POST'])
def fmyteams():
    if 'id' not in session:
        return redirect('../auth/login')
    if user.query.filter(user.user_id == session.get('id')).first().user_teamid==None:
        return redirect('teams')
    # 'cmd=' + pass + '&id=' + id
    # cmd == 0    ==> 无操作
    # cmd == 1    ==> 解散队伍
    # cmd == 2    ==> 移除队员[id]
    # cmd == 3    ==> 同意队员[id]加入战队
    # cmd == 4    ==> 拒绝队员[id]加入战队
    if request.method == 'POST':
        from CTF.models import db
        cmd = request.form.get('cmd')
        id = request.form.get('id')
        print(cmd, id)
        cmd =int(cmd)
        id=int(id)
        myself = user.query.filter(user.user_id == session.get('id')).first()
        print("$")
        if cmd == 1:
            oldteam = team.query.filter(team.team_id == myself.user_teamid).first()
            db.session.delete(oldteam)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            u = user.query.filter(user.user_id==myself.user_id).first()
            u.is_captain = 0
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return redirect('teams')
        if cmd==2:
            oldmate = user.query.filter(user.user_id == id).first()
            oldmate.user_teamid = None
            db.session.add(oldmate)
            db.session.commit()
            t = team.query.filter(team.team_id == myself.user_teamid).first()
            t.team_sum -= 1
            i = 1
            all_ans=[]
            while 1:
                u = user.query.filter(user.user_id == i ).first()
                if not u:
                    break
                if u.user_teamid != t.team_id:
                    i=i+1
                    continue
                for x in u.user_ans:
                    all_ans.append(x)
                i=i+1
            for one in t.team_ans:
                if not one in all_ans:
                    t.team_ans.remove(one)
            score=0
            for x in t.team_ans:
                score += x.que_score
            t.team_score = score          
            db.session.add(t)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
        if cmd==3:
            mate = user.query.filter(user.user_id == id).first()
            mate.is_captain = 0
            mate.user_teamid = myself.user_teamid
            t = team.query.filter(team.team_id == myself.user_teamid).first()
            t.team_sum += 1
            i = 1
            all_ans=[]
            while 1:
                u = user.query.filter(user.user_id == i ).first()
                if not u:
                    break
                if u.user_teamid != t.team_id:
                    i=i+1
                    continue
                for x in u.user_ans:
                    all_ans.append(x)
                i=i+1
            for one in all_ans:
                if not one in t.team_ans:
                    t.team_ans.append(one)
            score=0
            for x in t.team_ans:
                score += x.que_score
            t.team_score = score          
            db.session.add(t,mate)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
        if cmd == 4:
            mate = user.query.filter(user.user_id == id).first()
            mate.is_captain = 0
            mate.user_teamid = None
            db.session.add(mate)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    myself = user.query.filter(user.user_id == session.get('id')).first()
    t = team.query.filter(team.team_id == myself.user_teamid).first()
    allteams=[]
    i = 1 
    u = None
    while 1:
        u = user.query.filter(user.user_id == i).first()
        if not u:
            break
        if u.user_teamid!=myself.user_teamid:
            i+=1
            continue

        allteams.append({
        'id': u.user_id,
        'name': u.user_name,
        'score': u.user_score,
        'state': u.is_captain
        })
        i += 1
    name = session.get('username')          #用户名信息
    # return render_template('teams/my_team.html', allteams=allteams, team_name="adm1ns", team_score="10000") # 队员用户
    return render_template('teams/my_team.html', allteams=allteams, team_name=t.team_name, team_score=t.team_score, captain=myself.is_captain,name=name) # 队长用户
