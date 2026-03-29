import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base("works")
config = wiz.model("portal/works/config")
prefix = config.db_prefix

class Model(base):
    class Meta:
        db_table = prefix + "issueboard_mention"

    id = pw.CharField(max_length=32, primary_key=True)
    message_id = pw.BigIntegerField(index=True)
    issue_id = pw.CharField(max_length=32, index=True)
    user_id = pw.CharField(max_length=32, index=True)
    mentioned_user_id = pw.CharField(max_length=32, index=True)
    is_read = pw.BooleanField(default=False, index=True)
    created = pw.DateTimeField(index=True)
