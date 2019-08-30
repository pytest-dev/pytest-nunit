import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import enum


class CdataComment(ET.Element):
    def __init__(self, text):
        super(CdataComment, self).__init__("CDATA!")
        self.text = escape(text, {'\x1b': "&#x1b;"})


ET._original_serialize_xml = ET._serialize_xml


def _serialize_xml(write, elem, qnames, namespaces, *args, **kwargs):
    """
    Custom serializer to handle CdataComment classes
    """
    if isinstance(elem, CdataComment):
        write("<%s><%s%s]]></%s>" % (elem.tag, "![CDATA[", elem.text, elem.tag))
        return
    return ET._original_serialize_xml(write, elem, qnames, namespaces, *args, **kwargs)


class AttrsXmlRenderer(object):
    @staticmethod
    def as_element(i, name):
        el = ET.Element(name)
        if hasattr(i, "__attrs_attrs__"):
            for a in i.__attrs_attrs__:
                if a.metadata["type"] == "attrib" and getattr(i, a.name) is not None:
                    if isinstance(getattr(i, a.name), enum.Enum):
                        el.set(a.metadata["name"], getattr(i, a.name).name)
                    else:
                        el.set(a.metadata["name"], str(getattr(i, a.name)))
                if a.metadata["type"] == "content" and getattr(i, a.name) is not None:
                    el.text = str(getattr(i, a.name))
                if a.metadata["type"] == "element":
                    attrib = getattr(i, a.name)
                    if attrib is None and not a.metadata["optional"]:
                        ET.SubElement(el, a.metadata["name"])
                        continue
                    elif attrib is None and a.metadata["optional"]:
                        continue
                    if not isinstance(attrib, list):
                        attrib = [attrib]

                    for item in attrib:
                        # If subtype is an attrs instance, recurse
                        if hasattr(item, "__attrs_attrs__"):
                            el.append(
                                AttrsXmlRenderer.as_element(item, a.metadata["name"])
                            )
                        elif isinstance(item, ET.Element):
                            item.tag = a.metadata["name"]
                            el.append(item)
                        else:
                            ET.SubElement(el, a.metadata["name"]).text = str(item)

        return el

    @staticmethod
    def render(instance, node_name):
        root = AttrsXmlRenderer.as_element(instance, node_name)
        ET._serialize_xml = ET._serialize["xml"] = _serialize_xml
        s = ET.tostring(root, encoding="UTF-8", method="xml")
        return s
