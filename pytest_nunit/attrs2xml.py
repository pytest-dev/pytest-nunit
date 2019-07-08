import xml.etree.ElementTree as ET
import enum

class AttrsXmlRenderer(object):

    @staticmethod
    def as_element(i, name):
        el = ET.Element(name)
        if hasattr(i, '__attrs_attrs__'):
            for a in i.__attrs_attrs__:
                if a.metadata['type'] == 'attrib' and getattr(i, a.name) is not None:
                    if isinstance(getattr(i, a.name), enum.Enum):
                        el.set(a.metadata['name'], getattr(i, a.name).name)
                    else:
                        el.set(a.metadata['name'], str(getattr(i, a.name)))
                if a.metadata['type'] == 'element' and getattr(i, a.name) is not None:
                    # If subtype is an attrs instance, recurse
                    if hasattr(a.type, '__attrs_attrs__'):
                        el.append(AttrsXmlRenderer.as_element(getattr(i, a.name), a.metadata['name']))
                    else:
                        ET.SubElement(el, a.metadata['name']).text = str(getattr(i, a.name))

        return el

    @staticmethod
    def render(instance, node_name):
        root = AttrsXmlRenderer.as_element(instance, node_name)

        return ET.tostring(root, encoding="unicode", method="xml")
