import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "notification"

    id = pw.CharField(max_length=32, primary_key=True)
    user_id = pw.CharField(max_length=32, index=True)
    project_id = pw.CharField(max_length=32, default="")
    type = pw.CharField(max_length=32, index=True)
    ref_type = pw.CharField(max_length=16, default="")
    ref_id = pw.CharField(max_length=32, default="")
    title = pw.CharField(max_length=256, default="")
    message = pw.TextField(default="")
    is_read = pw.BooleanField(default=False, index=True)
    created = pw.DateTimeField(index=True)
    read_at = pw.DateTimeField(null=True)
