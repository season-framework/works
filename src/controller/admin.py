import season
import datetime
import json
import os

class Controller:
    def __init__(self):
        ctrl = wiz.controller("user")

        membership = wiz.session.get("membership")
        if membership not in ["admin", "superadmin"]:
            wiz.response.status(403, message="접근 권한이 없습니다")
