============
pytest-nunit
============

.. image:: https://github.com/pytest-dev/pytest-nunit/actions/workflows/ci.yml/badge.svg
    :target: https://pypi.org/project/pytest-nunit
    :alt: PyPI version
    
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

Requires:
- Pytest 5.1.0+
- Python 3.7+

Command-line options
--------------------

``--nunit-xml``
~~~~~~~~~~~~~~~

A string value to set the file name of the generated XML file.

Argument takes a path to the output file, either relative, or absolute.

``--nunit-prefix``
~~~~~~~~~~~~~~~~~~

A string value to prefix all test case names the string provided.

Defaults to an empty string.

INI Options
-----------

``nunit_show_username``
~~~~~~~~~~~~~~~~~~~~~~~

Boolean value to include the system username in the test run properties.

Defaults to ``false``

``nunit_show_user_domain``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Boolean value to include the system user domain in the test run properties.

Defaults to ``false``

``nunit_suite_name``
~~~~~~~~~~~~~~~~~~~~

(Deprecated, value ignored)

String value to set the test suite name.

Defaults to ``'pytest'``

``nunit_attach_on``
~~~~~~~~~~~~~~~~~~~~

Enumeration to control whether the attachments property is set on all test cases when the ``add_nunit_attachment`` is used.

Can be one of:

- ``any`` - Include test attachments for all outcomes (**Default**)
- ``pass`` - Include test attachments for only passed test cases
- ``fail`` - Include test attachments for only failed test cases

Fixtures
--------

The following fixtures are made available by this plugin.

``record_nunit_property``
~~~~~~~~~~~~~~~~~~~~~~~~~

Calling `record_nunit_property(key: str, value: str)` will result in `Property` tags being added to the `test-case` for the related node. 

.. code-block:: python

    def test_basic(record_nunit_property):
        record_nunit_property("test", "value")
        assert 1 == 1

``add_nunit_attachment``
~~~~~~~~~~~~~~~~~~~~~~~~

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


Compatibility with other plugins
--------------------------------

x-dist
~~~~~~

When running with `-f`, make sure to add in your pytest config file (setup.cfg etc)
`looponfailroots = testdir` to exclude xml report files from being watched for changes.

Check looponfails_


.. _looponfails: https://docs.pytest.org/en/3.0.1/xdist.html#running-tests-in-looponfailing-mode

