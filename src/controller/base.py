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
