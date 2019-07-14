============
pytest-nunit
============

.. image:: https://dev.azure.com/AnthonyShaw/pytest-nunit/_apis/build/status/tonybaloney.pytest-nunit?branchName=master
   :target: https://dev.azure.com/AnthonyShaw/pytest-nunit/_build/latest?definitionId=3?branchName=master
   :alt: Build status

.. image:: https://img.shields.io/pypi/v/pytest-nunit.svg
    :target: https://pypi.org/project/pytest-nunit
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-nunit.svg
    :target: https://pypi.org/project/pytest-nunit
    :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/pytest-nunit.svg
     :target: https://pypi.python.org/pypi/pytest-nunit/
     :alt: PyPI download month


A pytest plugin for generating Nunit3 test result XML output

This plugin is an early alpha release!

Configuration
-------------

Use ``--nunit-xml=output.xml`` to create an Nunit3-compatible file called ``output.xml``

Fixtures
--------

The following fixtures are made available by this plugin.

record_nunit_property
~~~~~~~~~~~~~~~~~~~~~

Calling `record_nunit_property(key: str, value: str)` will result in `Property` tags being added to the `test-case` for the related node. 

.. code-block:: python

    def test_basic(record_nunit_property):
        record_nunit_property("test", "value")
        assert 1 == 1

add_nunit_attachment
~~~~~~~~~~~~~~~~~~~~

Add an attachment to a node test-case by calling the `add_nunit_attachment()` function with the filepath and a description.

.. code-block:: python

    def test_attachment(add_nunit_attachment):
        pth = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
        add_nunit_attachment(path, "peanut butter jelly time")
        assert 1 == 1
