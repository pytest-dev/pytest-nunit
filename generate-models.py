"""
A script for generating attrs-models from an XSD.

Built especially for this model. But feel-free to reuse elsewhere.

Licensed under MIT. 
Written by Anthony Shaw.
"""

import click
import xmlschema


XS_ATOMIC_MAP = {
    '{http://www.w3.org/2001/XMLSchema}string': 'str',
    '{http://www.w3.org/2001/XMLSchema}int': 'int',
    '{http://www.w3.org/2001/XMLSchema}boolean': 'bool',
    '{http://www.w3.org/2001/XMLSchema}decimal': 'float'
}


def make_attrib(attrib):
    """
    Make attrs attribute from XmlAttribute
    :return: `str`
    """
    args = ['metadata={"name": \'%s\'}' % (attrib.name)]

    # Put type hints on XSD atomic types
    if isinstance(attrib.type, xmlschema.validators.XsdAtomicBuiltin):
        _atomic_type = XS_ATOMIC_MAP.get(attrib.type.name, 'object')
        args.append('type={0}'.format(_atomic_type))

        if attrib.use == 'required':
            args.append('validator=attr.validators.instance_of({0})'.format(_atomic_type))
    elif isinstance(attrib.type, xmlschema.validators.XsdAtomicRestriction):
        if attrib.use == 'required':
            args.append('validator=attr.validators.instance_of({0})'.format(attrib.type.name))

    # Set default value to none for optional args
    if attrib.use == 'optional':
        # Set all args to optional
        args.append('default=attr.NOTHING')

    name = attrib.name.replace('-', '_')

    return "{0} = attr.ib({1})".format(name, ', '.join(args))


@click.command()
@click.argument('xsd_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=False))
def main(xsd_path, output_path):
    xsd = xmlschema.XMLSchema(xsd_path)
    out = "import attr\n\n"
    for name, type_ in xsd.types.items():

        has_parts = False

        if isinstance(type_, xmlschema.validators.XsdComplexType):
            out += "@attr.s\nclass {0}(object):\n".format(name)

            for name, attrib in type_.attributes.items():
                out += "    {0}\n".format(make_attrib(attrib))
                has_parts = True
        elif isinstance(type_, xmlschema.validators.XsdAtomicRestriction):
            out += "@attr.s\nclass {0}({1}):\n".format(name, XS_ATOMIC_MAP.get(type_.base_type.name, 'object'))

        if not has_parts:
            out += "    pass\n"  # avoid having empty class

        out += "\n\n"

    # print(out)
    with open(output_path, "w") as out_f:
        out_f.write(out)


if __name__ == '__main__':
    main()