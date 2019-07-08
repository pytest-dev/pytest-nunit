"""
A script for generating attrs-models from an XSD.

Built especially for this model. But feel-free to reuse elsewhere.

Licensed under MIT. 
Written by Anthony Shaw.
"""

import logging
import click
import xmlschema
import xmlschema.qnames

logging.basicConfig()
log = logging.getLogger("__name__")
log.setLevel(logging.DEBUG)

KEYWORDS = ['id', 'type', 'class', 'if', 'else', 'and', 'for']

XS_ATOMIC_MAP = {
    xmlschema.qnames.XSD_STRING: 'str',
    xmlschema.qnames.XSD_INTEGER: 'int',
    xmlschema.qnames.XSD_INT: 'int',
    xmlschema.qnames.XSD_BOOLEAN: 'bool',
    xmlschema.qnames.XSD_DECIMAL: 'float'
}


def make_attrib(attrib, type_="attrib"):
    """
    Make attrs attribute from XmlAttribute
    :return: `str`
    """
    args = ['metadata={"name": \'%s\', "type": \'%s\'}' % (attrib.name, type_)]

    # Put type hints on XSD atomic types
    if isinstance(attrib.type, xmlschema.validators.XsdAtomicBuiltin):
        _atomic_type = XS_ATOMIC_MAP.get(attrib.type.name, 'object')
        args.append('type={0}'.format(_atomic_type))

        if hasattr(attrib, 'use') and attrib.use == 'required':
            args.append('validator=attr.validators.instance_of({0})'.format(_atomic_type))

    elif isinstance(attrib.type, xmlschema.validators.XsdAtomicRestriction):
        if hasattr(attrib, 'use') and attrib.use == 'required':
            if attrib.type.facets and xmlschema.qnames.XSD_ENUMERATION in attrib.type.facets:
                args.append('validator=attr.validators.in_({0})'.format(attrib.type.name))
            # If simple restriction type, use the base type instead (this isn't java)
            elif attrib.type.base_type.name in (XS_ATOMIC_MAP.keys()):
                args.append('validator=attr.validators.instance_of({0})'.format(
                    XS_ATOMIC_MAP.get(attrib.type.base_type.name, 'object')))
            else:
                args.append('validator=attr.validators.instance_of({0})'.format(attrib.type.name))

    elif isinstance(attrib.type, xmlschema.validators.XsdComplexType):
        args.append('type={0}'.format(attrib.type.name))
        args.append('validator=attr.validators.instance_of({0})'.format(attrib.type.name))

    if hasattr(attrib, 'use'):
        # Set default value to none for optional args
        if attrib.use == 'optional':
            # Set all args to optional
            args.append('default=attr.NOTHING')

    name = attrib.name.replace('-', '_')
    if name in KEYWORDS:
        name = name + '_'

    return "{0} = attr.ib({1})".format(name, ', '.join(args))


@click.command()
@click.argument('xsd_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=False))
def main(xsd_path, output_path):
    xsd = xmlschema.XMLSchema(xsd_path)
    out = "import attr\n" \
          "import enum\n\n\n"
    for name, type_ in xsd.types.items():

        has_parts = False

        # Write basic atomic restriction types
        if isinstance(type_, xmlschema.validators.XsdAtomicRestriction):
            is_enum_type = (type_.facets and xmlschema.qnames.XSD_ENUMERATION in type_.facets)

            if is_enum_type:
                out += "class {0}(enum.Enum):\n".format(name)
                enums = type_.facets[xmlschema.qnames.XSD_ENUMERATION].enumeration
                for e in enums:
                    out += "    {0} = '{0}'\n".format(e)
                has_parts = True
            else:
                out += "class {0}({1}):\n".format(
                    name,
                    XS_ATOMIC_MAP.get(type_.base_type.name, 'object'))

        # Write complex types as new attrs classes
        elif isinstance(type_, xmlschema.validators.XsdComplexType):
            log.info("Name %s" % name)
            out += "@attr.s\nclass {0}(object):\n".format(name)

            # Write element groups and sequences
            for group in type_.iter_components(xmlschema.validators.XsdGroup):
                if group.model == 'sequence':
                    for elem in group.iter_components(xmlschema.validators.XsdElement):
                        out += "    {0}\n".format(make_attrib(elem, "element"))
                        has_parts = True

            # Write element attributes
            for attrib in type_.attributes.values():
                out += "    {0}\n".format(make_attrib(attrib))
                has_parts = True

        if not has_parts:
            out += "    pass\n"  # avoid having empty class

        out += "\n\n"

    with open(output_path, "w") as out_f:
        out_f.write(out)


if __name__ == '__main__':
    main()