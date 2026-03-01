import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "calendar"

    id = pw.CharField(max_length=32, primary_key=True)
    project_id = pw.CharField(max_length=32, index=True)
    user_id = pw.CharField(max_length=32, index=True)
    title = pw.CharField(max_length=128)
    description = pw.TextField(default="")
    start = pw.DateTimeField(index=True)
    end = pw.DateTimeField(index=True)
    all_day = pw.BooleanField(default=False)
    color = pw.CharField(max_length=16, default="")
    category_id = pw.CharField(max_length=32, index=True, default="")
    status = pw.CharField(max_length=8, index=True, default="active")
    created = pw.DateTimeField()
    updated = pw.DateTimeField()
