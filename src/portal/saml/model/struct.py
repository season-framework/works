import os
import json
from flask import request
from season.util import stdClass
from season.util.filesystem import filesystem

import saml2
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from saml2.sigver import get_xmlsec_binary
from saml2.mdstore import MetadataStore
from saml2.attribute_converter import ac_factory

class Struct:
    def __init__(self):
        self.fs = filesystem(wiz.project.path("config/saml")[len(wiz.path("")):])

        self.metadata = wiz.model("portal/saml/struct/metadata")(self)
        self.md = self.metadata
        self.process = wiz.model("portal/saml/struct/process")(self)
        self.attributes = wiz.model("portal/saml/struct/attributes")(self)
        self.attr = self.attributes
        self.base_domain = request.url_root.rstrip('/').replace("http://", "https://")
    
    def handler(self, idp):
        cfg = self.config()
        xml_path = self.fs.abspath(f'{idp}.xml')
        db = wiz.model("portal/season/orm").use("saml_idp", module="saml")
        idp_info = db.get(key=idp, use=True)
        if idp_info is None:
            wiz.response.abort(404)
        # acs = ac_factory(wiz.project.path("src/portal/saml/model/ac_factory_custom"))
        acs = ac_factory()
        mdStore = MetadataStore(acs, cfg)
        xml_md_string = idp_info["xml_content"]
        mdStore.load("inline", xml_md_string)
        cfg.metadata = mdStore
        cfg.allow_unknown_attributes = True
        client = Saml2Client(config=cfg)
        return client

    def config_from_db(self):
        orm = wiz.model("portal/season/orm")
        db = orm.use("saml_sp_config", module="saml")
        rows = db.rows()
        to_json = ["NameIDFormat", "required_attributes", "optional_attributes", "contact", "org"]
        to_boolean = ["AuthnRequestSigned", "WantAssertionsSigned"]
        config = dict()
        for row in rows:
            config[row["key"]] = row["value"]

        # to json
        for key in to_json:
            if key not in config: continue
            val = config[key]
            try: config[key] = json.loads(val)
            except: pass

        # boolean
        for key in to_boolean:
            if key not in config: continue
            val = config[key]
            config[key] = True if val.lower() == "true" else False

        return config

    def config(self, key=None):
        xmlsec_path = get_xmlsec_binary(["/usr/bin/xmlsec1"])
        season_config = wiz.config("season")
        saml_mode = season_config.get("saml_mode", "config") # config / db
        if saml_mode == "config":
            saml_config = season_config.get("saml")
        else: # db
            saml_config = self.config_from_db()
        saml_config = stdClass(saml_config)

        origin = self.base_domain
        acs_endpoint = saml_config.get("acs", '/auth/saml/acs')
        sls_endpoint = saml_config.get("sls", '/auth/saml/acs')

        public_key = saml_config.public_key
        if not public_key.startswith("/"): public_key = self.fs.abspath(public_key)
        private_key = saml_config.private_key
        if not private_key.startswith("/"): private_key = self.fs.abspath(private_key)

        config = {
            'entityid': saml_config.entityID,
            'name': saml_config.name,
            'description': saml_config.description,
            'service': {
                'sp': {
                    'name': saml_config.name,
                    'endpoints': {
                        'assertion_consumer_service': [
                            (f"{origin}{acs_endpoint}", saml2.BINDING_HTTP_POST),
                            (f"{origin}{acs_endpoint}", saml2.BINDING_HTTP_REDIRECT),
                        ],
                        "single_logout_service": [
                            (f"{origin}{sls_endpoint}", saml2.BINDING_HTTP_REDIRECT),
                        ],
                    },
                    "allow_unsolicited": True,
                    'required_attributes': saml_config.required_attributes,
                    'optional_attributes': saml_config.optional_attributes,
                    'authn_requests_signed': saml_config.AuthnRequestSigned,
                    'want_assertions_signed': saml_config.WantAssertionsSigned,
                    'name_id_format': saml_config.NameIDFormat,
                }
            },
            'cert_file': public_key,
            'key_file': private_key,
            'contact_person': [
                {
                    'given_name': saml_config.contact.name,
                    'email_address': saml_config.contact.email,
                    'contact_type': saml_config.contact.type,
                },
            ],
            'organization': {
                'name': saml_config.org.name,
                'display_name': saml_config.org.display_name,
                'url': saml_config.org.url,
            },
            'xmlsec_binary': xmlsec_path,
        }
        cfg = Saml2Config()
        cfg.load(config)
        return cfg

Model = Struct()
