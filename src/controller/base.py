import season
import datetime
import json
import os
from flask import request

class Controller:
    def __init__(self):
        wiz.session = wiz.model("portal/season/session").use()
        sessiondata = wiz.session.get()
        wiz.response.data.set(session=sessiondata)

        # 강제 로그아웃된 세션 차단
        forced_logout = False
        session_token = wiz.session.get("session_token")
        if session_token:
            try:
                orm = wiz.model("portal/season/orm")
                session_db = orm.use("user_session", id_size=64)
                sess = session_db.get(id=session_token)
                if sess and not sess['is_active']:
                    forced_logout = True
            except: pass

        if forced_logout:
            wiz.session.clear()
            wiz.response.status(401)
        
        def query(key=None, default=None):
            method = wiz.request.method().upper()
            if method == "GET":
                body = request.args.to_dict()
            else:
                try:
                    body = request.get_json()
                except Exception as e:
                    body = dict(request.values)

            if key is None: return body
            if key not in body:
                if type(default) == bool and default == True:
                    wiz.response.abort(400)
                return default
            return body[key]
        wiz.request.query = query

        lang = wiz.request.query("lang", None)
        if lang is not None:
            print("[keycloud] set language", lang)
            wiz.response.lang(lang)
            wiz.response.redirect(wiz.request.uri())

    def json_default(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return str(value).replace('<', '&lt;').replace('>', '&gt;')
