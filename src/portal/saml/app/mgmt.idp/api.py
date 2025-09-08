import datetime

orm = wiz.model("portal/season/orm")
db = orm.use("saml_idp", module="saml")

def load():
    rows = db.rows(fields="id,key,display_name,use,icon,created,updated")
    wiz.response.status(200, rows)

def xml():
    id = wiz.request.query("id", None)
    row = db.get(id=id)
    if row is None:
        wiz.response.abort(404)
    wiz.response.status(200, row["xml_content"])

def update():
    id = wiz.request.query("id", None)
    data = wiz.request.query()
    if id is None:
        db.insert(data)
    else:
        data["updated"] = datetime.datetime.now()
        db.update(data, id=id)
    wiz.response.status(200)

def remove():
    key = wiz.request.query("key", True)
    db.delete(key=key)
    wiz.response.status(200)
