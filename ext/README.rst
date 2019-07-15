External Data Models
====================

This directory contains copies of the NUnit XSD documents used to both generate this library and validate the output.

The ``nunit-model`` directory contains a hand-written XSD document to describe the test run and is used by ``generate-models.py`` to create the ``models/nunit.py`` set of data classes.

The model is a simplified version of the original, with ``complexType`` separated into a top-level named type, instead of being embedded in element definitions.

This makes the auto-generated classes easier to use and named logically.

The ``nunit-src`` directory contains a copy of the Nunit3 XSD files from the Nunit3 source code. However, the ones in source contain errors, such as attachments being contained with an assertions element (which they aren't), so changes have been made to correlate it to the documentation.

The Nunit3 documentation is the closest thing to a reference, however they don't provide a master XSD.

The src XSD files are used by the integration tests to validate any XML files produced by the plugin and prove very useful.

``generate-models.py``
----------------------

This script is used for generating Python models from an XSD document.

It looks at an XSD document to find complexType's and creates attrs classes for each corresponding type.

- ``xs:choice`` elements will be marked as optional,
- ``xs:sequence`` will be marked as required, unless they have ``minOccurs=0``
- Atomic types will be mapped to Python builtin types
- Simple Types will be mapped to their inherited atomic type
- Enumeration types will be created as ``enum`` classes
- Output will be formatting using the black 19.0 API

To regenerate the models for the nunit-models:

   python ext/generate-models.py ext/nunit-model/TestResult.xsd pytest_nunit/models/nunit.py

