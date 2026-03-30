import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "push_subscription"

    id = pw.CharField(max_length=32, primary_key=True)
    user_id = pw.CharField(max_length=32, index=True)
    endpoint = pw.TextField()
    p256dh = pw.TextField()
    auth = pw.CharField(max_length=128)
    user_agent = pw.TextField(default="")
    created = pw.DateTimeField()
    updated = pw.DateTimeField()
