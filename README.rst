============
pytest-nunit
============

.. image:: https://pytest-dev.visualstudio.com/pytest-nunit/_apis/build/status/pytest-dev.pytest-nunit?branchName=master
   :target: https://pytest-dev.visualstudio.com/pytest-nunit/_build/latest?definitionId=7&branchName=master
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

Requires:
- Pytest 4.6+
- Python 3.6+

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


History
-------

0.6.0 (4th August 2020)
~~~~~~~~~~~~~~~~~~~~~~~

- fix unicode escapes in cdata (#39)
- fix start/stop time calculation (#42)
- dropping support for python3.4 (#45)
- dropping support for old xdist versions (#44)

0.5.3 (15th April 2020)
~~~~~~~~~~~~~~~~~~~~~~~

- Bugfix - Fix time taken for tests under certain scenarios causing crash on pytest_sessionfinish

0.5.2 (30th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~

- Bugfix - Escape tabbed unicode characters from stdout feed from being in CDATA output

0.5.1 (30th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~

- Bugfix - Fixed cause of crash for tests that could be discovered but never executed

0.5.0 (30th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~

- Docstrings of nodes (functions) are set as the label for TestCase elements (contribution by @mikeattara)
- Pytest -k keyword filters are added to the test run filter element under ``name``.
- Pytest -m marker filters are added to the test run filter element under ``namespace``.
- Any path filters are added to the test run filter element under ``test``.
- Each Python module containing tests is now a separate ``test-suite`` element, instead of having one large suite
- Docstrings of modules are set as the label for TestSuite elements

0.4.0 (28th August 2019)
~~~~~~~~~~~~~~~~~~~~~~~~

- Added user domain (contribution by @williano)
- Added tests and help for xdist execution (contribution by @mei-li)
- Dynamically use the keyword list when generating schema to avoid reserved word collision (contribution by @gerhardtdatsomor)
- Add method names, classnames and module names to output (contribution by @adekanyetomie)
- Added locale and uiculture properties to runtime output (contribution by @terrameijar)
- Added ``nunit_attach_on`` INI option to control when attachments are included in test cases.

0.3.0 (15th July 2019)
~~~~~~~~~~~~~~~~~~~~~~

- Added ``--nunit-prefix`` option.

0.2.1 (15th July 2019)
~~~~~~~~~~~~~~~~~~~~~~

- First stable release
