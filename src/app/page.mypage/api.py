import json
import re
import datetime

config = wiz.model("portal/season/config")

orm = wiz.model("portal/season/orm")
db = orm.use("user")

def session():
    resp = dict()
    user_id = wiz.session.get("id")
    user = db.get(id=user_id)
    if user['password'] is None:
        user['hasPassword'] = False
    else:
        user['hasPassword'] = True
    del user['password']
    resp['user'] = user
    
    config.session_create(wiz, user_id)
    wiz.response.status(200, **resp)

def update():
    user = json.loads(wiz.request.query("userinfo", True))
    allowed = ['name', 'mobile', 'profile_image']
    update_data = {k: user[k] for k in allowed if k in user}
    if len(update_data) == 0:
        wiz.response.status(400, "수정할 항목이 없습니다")
    user_id = wiz.session.get("id")
    db.update(update_data, id=user_id)
    wiz.response.status(200, True)

def change_password():
    current = wiz.request.query("current", True)
    data = wiz.request.query("data", True)
    user_id = wiz.session.get("id")
    user = db.get(id=user_id)

    if user['password'] is not None:
        if user['password'](current) == False:
            wiz.response.status(401, "비밀번호가 틀렸습니다")
    
    db.update(dict(password=data), id=user_id)
    wiz.response.status(200, True)

def login_history():
    user_id = wiz.session.get("id")
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))

    history_db = orm.use("login_history")
    total = history_db.count(user_id=user_id)
    rows = history_db.rows(
        user_id=user_id,
        orderby="created",
        order="DESC",
        page=page,
        dump=dump,
        fields="id,ip,device_name,login_method,status,created"
    )

    # datetime 직렬화
    for row in rows:
        if isinstance(row.get('created'), datetime.datetime):
            row['created'] = row['created'].strftime('%Y-%m-%d %H:%M:%S')

    wiz.response.status(200, rows=rows, total=total, page=page)

def active_sessions():
    user_id = wiz.session.get("id")
    current_token = wiz.session.get("session_token")

    session_db = orm.use("user_session", id_size=64)
    rows = session_db.rows(
        user_id=user_id,
        is_active=True,
        orderby="last_active",
        order="DESC",
        fields="id,device_name,ip,created,last_active"
    )

    for row in rows:
        row['is_current'] = (row['id'] == current_token)
        if isinstance(row.get('created'), datetime.datetime):
            row['created'] = row['created'].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(row.get('last_active'), datetime.datetime):
            row['last_active'] = row['last_active'].strftime('%Y-%m-%d %H:%M:%S')

    wiz.response.status(200, sessions=rows)

def force_logout():
    user_id = wiz.session.get("id")
    session_id = wiz.request.query("session_id", True)
    current_token = wiz.session.get("session_token")

    # 현재 세션은 강제 종료 불가
    if session_id == current_token:
        wiz.response.status(400, message="현재 세션은 강제 종료할 수 없습니다")

    session_db = orm.use("user_session", id_size=64)
    target = session_db.get(id=session_id)

    if target is None:
        wiz.response.status(404, message="세션을 찾을 수 없습니다")

    # 본인 세션만 종료 가능
    if target['user_id'] != user_id:
        wiz.response.status(403, message="권한이 없습니다")

    session_db.update(dict(is_active=False), id=session_id)
    wiz.response.status(200, True)

def force_logout_all():
    user_id = wiz.session.get("id")
    current_token = wiz.session.get("session_token")

    session_db = orm.use("user_session", id_size=64)
    rows = session_db.rows(user_id=user_id, is_active=True, fields="id")

    count = 0
    for row in rows:
        if row['id'] == current_token:
            continue
        session_db.update(dict(is_active=False), id=row['id'])
        count += 1

    wiz.response.status(200, count=count)
