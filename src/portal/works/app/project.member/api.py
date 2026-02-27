import json

orm = wiz.model("portal/season/orm")
db = orm.use("user")

def search():
    keyword = wiz.request.query("keyword", "")
    keyword = keyword.strip()
    exclude = wiz.request.query("exclude", "")

    exclude_list = []
    if exclude:
        exclude_list = [e.strip() for e in exclude.split(",") if e.strip()]

    def query(Model, qs):
        cond = (Model.status.in_(['active', 'pending']))
        if len(keyword) > 0:
            cond = cond & ((Model.name.contains(keyword)) | (Model.email.contains(keyword)))
        if exclude_list:
            cond = cond & (~Model.email.in_(exclude_list))
        qs = qs.where(cond)
        return qs

    rows = db.rows(query=query, orderby="name", dump=20)

    internal = []
    external = []
    for row in rows:
        item = dict(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            membership=row['membership']
        )
        if row['membership'] in ['admin', 'staff']:
            internal.append(item)
        else:
            external.append(item)

    wiz.response.status(200, internal=internal, external=external)
