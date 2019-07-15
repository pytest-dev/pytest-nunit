============
pytest-nunit
============

.. image:: https://dev.azure.com/AnthonyShaw/pytest-nunit/_apis/build/status/pytest-dev.pytest-nunit?branchName=master
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


A pytest plugin for generating NUnit3 test result XML output

This plugin is an early beta release!

Configuration
-------------

--nunit-xml
~~~~~~~~~~~

Use ``--nunit-xml=output.xml`` to create an NUnit3-compatible file called ``output.xml``

Argument takes a path to the output file, either relative, or absolute.

--nunit-prefix
~~~~~~~~~~~~~~

Use ``--nunit-prefix=example-`` to prefix all test case names with ``"example-"``


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

Add an attachment to a node test-case by calling the `add_nunit_attachment(path: str, description: str)` function with the filepath and a description.

.. code-block:: python

    def test_attachment(add_nunit_attachment):
        pth = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
        add_nunit_attachment(path, "peanut butter jelly time")
        assert 1 == 1

Usage with Azure Pipelines
--------------------------

Add the following steps to your build job to publish the results to Azure Pipelines:

.. code-block:: yaml

      - script: "pip install pytest-nunit"

      - script: |
          python -m pytest tests -v --nunit-xml=test-results.xml
        continueOnError: true

      - task: PublishTestResults@2
        inputs:
          testResultsFormat: NUnit
          testResultsFiles: '**/test-results.xml'

Skipped Tests
~~~~~~~~~~~~~

Skipped tests will have the ``reason`` attribute (if provided) included in the results.

.. image:: https://github.com/pytest-dev/pytest-nunit/raw/master/docs/source/_static/screen_skips.png
   :width: 70%


Attachments
~~~~~~~~~~~

Using the ``add_nunit_attachment`` fixture will render any attachments in the "attachments" tab inside the Tests console:

.. image:: https://github.com/pytest-dev/pytest-nunit/raw/master/docs/source/_static/screen_attachments.png
   :width: 70%

Failures and xfails
~~~~~~~~~~~~~~~~~~~

Any failed tests, whether as xpass or xfail, will have the error output and comparison, as well as the failing line in the stack trace.

.. image:: https://github.com/pytest-dev/pytest-nunit/raw/master/docs/source/_static/screen_fails.png
   :width: 70%

History
-------

0.3.0 (15th July)
=================

- Added ``--nunit-prefix`` option.

0.2.1 (15th July)
=================

- First stable release
