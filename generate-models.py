"""
A script for generating attrs-models from an XSD.

Built especially for this model. But feel-free to reuse elsewhere.

Licensed under MIT. 
Written by Anthony Shaw.
"""

import click
import xmlschema


@click.command()
@click.argument('xsd_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=False))
def main(xsd_path, output_path):
    xsd = xmlschema.XMLSchema(xsd_path)
    print(xsd)

if __name__ == '__main__':
    main()