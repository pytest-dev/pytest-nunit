External Data Models
====================

This directory contains copies of the NUnit XSD documents used to both generate this library and validate the output.

The ``nunit-model`` directory contains a hand-written XSD document to describe the test run and is used by ``generate-models.py`` to create the ``models/nunit.py`` set of data classes.

The model is a simplified version of the original, with ``complexType`` separated into a top-level named type, instead of being embedded in element definitions.

This makes the auto-generated classes easier to use and named logically.

The ``nunit-src`` directory contains a copy of the Nunit3 XSD files from the Nunit3 source code. However, the ones in source contain errors, such as attachments being contained with an assertions element (which they aren't), so changes have been made to correlate it to the documentation.

The Nunit3 documentation is the closest thing to a reference, however they don't provide a master XSD.

The src XSD files are used by the integration tests to validate any XML files produced by the plugin and prove very useful.