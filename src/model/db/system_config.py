import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base()

class Model(base):
    class Meta:
        db_table = 'system_config'

    id = pw.CharField(max_length=32, primary_key=True)
    category = pw.CharField(max_length=32, index=True)
    key_name = pw.CharField(max_length=64, index=True)
    value = pw.TextField(null=True)
    value_type = pw.CharField(max_length=16, default='string')
    description = pw.CharField(max_length=255, null=True)
    updated = pw.DateTimeField()
