import season
import datetime
import json
import os

class Controller:
    def __init__(self):
        ctrl = wiz.controller("base")

        user_id = wiz.session.get("id")
        if user_id is None:
            config = wiz.model("portal/season/config")
            login_uri = config.auth_login_uri
            if login_uri is None:
                login_uri = "/authenticate"
            current_uri = wiz.request.uri()
            wiz.response.redirect(f"{login_uri}?returnTo={current_uri}")
