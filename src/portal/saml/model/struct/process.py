import saml2
from saml2.saml import AuthnContextClassRef
import datetime

def get_location(headers):
    location = None
    for k, v in headers:
        if k == "Location":
            location = v
            break
    return location

class Process:
    def __init__(self, core):
        self.core = core

    def login(
        self,
        idp,
        authnContextRef=None,
        entityid=None,
    ):
        if authnContextRef is None:
            authnContextRef = "urn:oasis:names:tc:SAML:2.0:ac:classes:Password"

        handler = self.core.handler(idp)

        authn_context = saml2.samlp.RequestedAuthnContext(
            authn_context_class_ref=[AuthnContextClassRef(text=authnContextRef)],
            comparison="exact",
        )

        if entityid is None: # single
            reqid, info = handler.prepare_for_authenticate(
                requested_authn_context=authn_context
            )
        else: # federation
            binding, destination = handler.pick_binding(
                "single_sign_on_service",
                entity_id=entityid,
            )
            reqid, info = handler.prepare_for_authenticate(
                entityid=entityid,
                binding=binding,
                requested_authn_context=authn_context,
            )

        wiz.session.set(
            reqid=reqid,
            idp=idp,
            authnContextRef=authnContextRef,
        )

        redirect_url = get_location(info["headers"])
        wiz.response.redirect(redirect_url)

    def acs(self, SAMLResponse):
        request_id = wiz.session.get("reqid")
        idp = wiz.session.get("idp", "season")
        authnContextRef = wiz.session.get("authnContextRef")

        handler = self.core.handler(idp)
        try:
            authn_response = handler.parse_authn_request_response(
                SAMLResponse,
                saml2.BINDING_HTTP_POST,
                outstanding={request_id: dict()},
            )
        except:
            print("[process] expired response")
            wiz.response.abort(401)

        attributes = authn_response.get_identity()
        userinfo = dict()
        for key in attributes:
            value = attributes[key]
            if type(value) == list:
                if len(value) > 0:
                    userinfo[key] = value[0]
            else:
                userinfo[key] = value

        saml_acs = wiz.config("season").get("saml_acs")
        if saml_acs is not None:
            sessiondata = saml_acs(wiz, userinfo)
        else:
            sessiondata = userinfo

        wiz.session.set(**sessiondata)
        wiz.response.redirect("/dashboard")

    def logout(self, returnTo="/authenticate"):
        wiz.session.clear()
        wiz.response.redirect(returnTo)

Model = Process
