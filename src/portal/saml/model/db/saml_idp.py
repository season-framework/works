import peewee as pw
orm = wiz.model("portal/season/orm")
base = orm.base()

class Model(base):
    class Meta:
        db_table = "saml_idp"

    id = pw.CharField(max_length=32, primary_key=True)
    key = pw.CharField(max_length=64)
    display_name = pw.CharField(max_length=255)
    use = pw.BooleanField(default=True)
    xml_content = pw.TextField()
    icon = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()

'''
create or replace table saml_idp
(
    id           varchar(32)                            not null,
    `key`        varchar(64)                            not null,
    display_name varchar(255)                           null,
    `use`        tinyint(1) default 1                   not null,
    xml_content  longtext   default ''                  not null,
    icon         longtext                               null,
    created      timestamp  default current_timestamp() null,
    updated      timestamp  default current_timestamp() not null,
    primary key (id),
    constraint `key`
        unique (`key`)
)
    collate = utf8mb4_unicode_ci;
'''
