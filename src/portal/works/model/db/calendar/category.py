import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "calendar_category"

    id = pw.CharField(max_length=32, primary_key=True)
    project_id = pw.CharField(max_length=32, index=True)
    name = pw.CharField(max_length=64)
    color = pw.CharField(max_length=16, default="#3b82f6")
    sort_order = pw.IntegerField(default=0)
    status = pw.CharField(max_length=8, index=True, default="active")
    created = pw.DateTimeField()
    updated = pw.DateTimeField()
