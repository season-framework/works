import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "calendar_attendee_group"

    id = pw.CharField(max_length=32, primary_key=True)
    event_id = pw.CharField(max_length=32, index=True)
    project_id = pw.CharField(max_length=32, index=True)
    group_type = pw.CharField(max_length=16, index=True)
    group_id = pw.CharField(max_length=32, default="")
    created = pw.DateTimeField()
