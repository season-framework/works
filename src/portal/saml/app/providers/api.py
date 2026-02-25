
def load():
    orm = wiz.model("portal/season/orm")
    db = wiz.model("portal/season/orm").use("saml_idp", module="saml")
    rows = db.rows(use=True, fields="key,display_name,icon")
    wiz.response.status(200, rows)
