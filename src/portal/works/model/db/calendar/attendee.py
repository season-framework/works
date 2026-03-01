import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "calendar_attendee"

    id = pw.CharField(max_length=32, primary_key=True)
    event_id = pw.CharField(max_length=32, index=True)
    user_id = pw.CharField(max_length=32, index=True)
    project_id = pw.CharField(max_length=32, index=True)
    status = pw.CharField(max_length=8, default="accepted")
    created = pw.DateTimeField()
