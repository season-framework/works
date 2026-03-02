import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base()

class Model(base):
    class Meta:
        db_table = 'login_history'

    id = pw.CharField(max_length=32, primary_key=True)
    user_id = pw.CharField(max_length=32, index=True)
    email = pw.CharField(max_length=255)
    ip = pw.CharField(max_length=64)
    user_agent = pw.TextField()
    device_name = pw.CharField(max_length=128)
    login_method = pw.CharField(max_length=32)
    status = pw.CharField(max_length=16)
    created = pw.DateTimeField()
