"""
A script for generating attrs-models from an XSD.

Built especially for this model. But feel-free to reuse elsewhere.

Licensed under MIT. 
Written by Anthony Shaw.
"""

import click
import xmlschema


XS_ATOMIC_MAP = {
    'xs:string': 'str',
    'xs:int': 'object'
}


def make_attrib(attrib):
    """
    Make attrs attribute from XmlAttribute
    :return: `str`
    """
    args = []
    if isinstance(attrib.type, xmlschema.validators.XsdAtomicBuiltin):
        args.append('type={0}'.format(XS_ATOMIC_MAP.get(attrib.type.name, 'object')))
    return "attr.ib({0})".format(','.join(args))


@click.command()
@click.argument('xsd_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=False))
def main(xsd_path, output_path):
    xsd = xmlschema.XMLSchema(xsd_path)
    out = "import attr\n\n"
    for name, type_ in xsd.types.items():
        out += "@attr.s\nclass {0}(object):\n".format(name)
        if isinstance(type_, xmlschema.validators.XsdComplexType):
            for name, attrib in type_.attributes.items():
                out += "    {0} = {1}\n".format(name, make_attrib(attrib))
        out += "\n\n"

    print(out)
    with open(output_path, "w") as out_f:
        out_f.write(out)

if __name__ == '__main__':
    main()