import json

# NOTE: portal/modules 패키지가 현재 프로젝트에 존재하지 않음 (레거시 코드)
# 아래 함수들은 프론트엔드에서 호출되지 않으므로 비활성 상태
try:
    Struct = wiz.model("portal/modules/struct")
except Exception:
    Struct = None

def load_menu():
    if Struct is None:
        wiz.response.status(200, [])
    mod = Struct("util", "mysql")
    config = mod.lib.config.Config()
    menus = config.get("custom_menu", "[]")
    menus = json.loads(menus)
    wiz.response.status(200, menus)

def request_count():
    if Struct is None:
        wiz.response.status(200, 0)
    mod = Struct("core", "request")
    db = mod.db(mod.model.request)
    count = db.count(ref=None, response_by=None)
    wiz.response.status(200, count)

