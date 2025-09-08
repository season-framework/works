from season.util.filesystem import filesystem

from saml2.metadata import metadata_tostring_fix, NSPAIR
from saml2.metadata import entity_descriptor
# from saml2.metadata import create_metadata_string
import xml.etree.ElementTree as ET

class Metadata:
    def __init__(self, core):
        self.core = core
        self.filename = "sp.xml"

    def myself(self, create=False):
        fs = self.core.fs
        if fs.exists(self.filename) == False or create == True:
            config = self.core.config()
            self.create_myself(config)
        return fs.read(self.filename, "")

    def create_myself(self, config):
        eds = entity_descriptor(config)
        xml_string = metadata_tostring_fix(eds, NSPAIR)
        if isinstance(xml_string, str):
            xml_string = xml_string.encode('utf-8')
        if isinstance(xml_string, bytes):
            xml_string = xml_string.decode('utf-8')
        # xml_string = create_metadata_string(None, config=config, sign=True)
        try:
            root = ET.fromstring(xml_string)
            tree = ET.ElementTree(root)
            ET.indent(tree, space='  ')
            xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
            if not xml_string.startswith('<?xml'):
                xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_string
        except:
            pass
        print(f"SP Metadata created")
        self.core.fs.write(self.filename, xml_string)

Model = Metadata
