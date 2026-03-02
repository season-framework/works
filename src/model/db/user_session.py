import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base()

class Model(base):
    class Meta:
        db_table = 'user_session'

    id = pw.CharField(max_length=64, primary_key=True)
    user_id = pw.CharField(max_length=32, index=True)
    ip = pw.CharField(max_length=64)
    user_agent = pw.TextField()
    device_name = pw.CharField(max_length=128)
    is_active = pw.BooleanField(default=True)
    created = pw.DateTimeField()
    last_active = pw.DateTimeField()
