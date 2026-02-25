import json
import saml2.attributemaps.saml_uri as saml_map

struct = wiz.model("portal/saml/struct")
fs = struct.fs

to_json = ["NameIDFormat", "required_attributes", "optional_attributes", "contact", "org"]
to_boolean = ["AuthnRequestSigned", "WantAssertionsSigned"]

def load():
    config = struct.config_from_db()

    if "public_key" in config:
        _path = config["public_key"]
        exists = fs.exists(_path)
        config["public_key"] = dict(
            path=_path,
            exists=exists,
        )
        if exists: config["public_key"]["content"] = fs.read(_path)
    else:
        config["public_key"] = dict(exists=False)

    if "private_key" in config:
        _path = config["private_key"]
        config["private_key"] = dict(
            path=_path,
            exists=fs.exists(_path),
        )
    else:
        config["private_key"] = dict(exists=False)

    wiz.response.status(200, config=config, saml_attributes=struct.attr.get())

def update():
    config = wiz.request.query()
    orm = wiz.model("portal/season/orm")
    db = orm.use("saml_sp_config", module="saml")
    db.delete()
    for key, value in config.items():
        if key in to_json: value = json.dumps(value)
        if key in to_boolean: config[key] = "true" if value is True else "false"
        db.insert(dict(key=key, value=value))
    struct.md.myself(create=True)
    wiz.response.status(200)
