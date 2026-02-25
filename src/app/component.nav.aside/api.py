import json

Struct = wiz.model("portal/modules/struct")

def load_menu():
    mod = Struct("util", "mysql")
    config = mod.lib.config.Config()
    menus = config.get("custom_menu", "[]")
    menus = json.loads(menus)
    wiz.response.status(200, menus)

def request_count():
    mod = Struct("core", "request")
    db = mod.db(mod.model.request)
    count = db.count(ref=None, response_by=None)
    wiz.response.status(200, count)

