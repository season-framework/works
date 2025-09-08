BASE_URL = wiz.request.request().url.split(wiz.request.uri())[0]
BASE = "/saml"
uri = wiz.request.uri()[len(BASE):]
if uri.startswith("/"): uri = uri[1:]
path = uri.split("/")

struct = wiz.model("portal/saml/struct")

if uri == "metadata":
    create = True if wiz.request.query("new", "false") == "true" else False
    metadata = struct.md.myself(create)
    wiz.response.send(metadata, "application/xml")

if uri == "login":
    idp = wiz.request.query("idp", True)
    struct.process.login(idp)

if uri == "acs":
    SAMLResponse = wiz.request.query("SAMLResponse", True)
    struct.process.acs(SAMLResponse)

if uri == "logout" or uri == "sls":
    returnTo = wiz.request.query("returnTo", "/authenticate")
    struct.process.logout(returnTo)

