import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base()

class Model(base):
    class Meta:
        db_table = "saml_sp_config"

    id = pw.CharField(max_length=32, primary_key=True)
    key = pw.CharField(max_length=64)
    value = pw.TextField()

'''
create or replace table saml_sp_config
(
    id           varchar(32)                            not null,
    `key`        varchar(64)                            not null,
    `value`  longtext   default ''                  not null,
    primary key (id)
)
    collate = utf8mb4_unicode_ci;
'''
