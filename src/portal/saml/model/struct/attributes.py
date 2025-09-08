import saml2.attributemaps.saml_uri as saml_map

excludes = [
    "PVP-GID",
    "PVP-BPK",
    "PVP-OU-OKZ",
    "PVP-VERSION",
    "PVP-PRINCIPAL-NAME",
    "PVP-PARTICIPANT-OKZ",
    "PVP-ROLES",
    "PVP-INVOICE-RECPT-ID",
    "PVP-COST-CENTER-ID",
    "PVP-CHARGE-CODE",
    "PVP-OU-GV-OU-ID",
    "PVP-FUNCTION",
    "PVP-BIRTHDATE",
    "PVP-PARTICIPANT-ID",
    "PVP-USERID",
    "PVP-MAIL",
    "PVP-OU",
    "PVP-TEL",
    "PVP-GIVENNAME",
]

class Attributes:
    def __init__(self, core):
        self.core = core

    def __sorted__(self, rows):
        return sorted(
            rows,
            key=lambda x: (
                0 if "id" in x else 1,
                0 if x["uri"].startswith("urn:oid:") else 1,
                0 if x["uri"].startswith("urn:") else 1,
                x["uri"],
            ),
        )

    def get(self):
        data = saml_map.MAP["to"]
        res = []
        for name, uri in data.items():
            if name in excludes:
                continue
            res.append(dict(name=name, uri=uri))
        res = self.__sorted__(res)
        return res

Model = Attributes
