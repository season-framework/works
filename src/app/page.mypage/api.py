import json
import re

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
