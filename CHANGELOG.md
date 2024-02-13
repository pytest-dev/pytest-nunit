# Changelog

## 1.0.6 (13th February 2024)

* replace deprecated datetime.utcnow() functionality by @dijkstrar in https://github.com/pytest-dev/pytest-nunit/pull/72
* Backward compatible version of the datetime.UTC attribute by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/76

## 1.0.5 (13th February 2024)

* Mute deprecation warning of getdefaultlocale until a better solution by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/74

## 1.0.4 (11th October 2023)

* Support for Python 3.12

## 1.0.3 (20th October 2022)

* Fixes bug when used with xdist extension by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/66

## 1.0.2 (19th October 2022)

* Don't assert that call-report exists before checking value of attribute by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/63
* Fix crash when ExceptionReprGroup is set for trace in test case by @gh-ppolk in https://github.com/pytest-dev/pytest-nunit/pull/65
* [minor] Add xmlschema dev dependency by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/62
* [minor] Add plugin coverage by @tonybaloney in https://github.com/pytest-dev/pytest-nunit/pull/64

## 1.0.1 (26th July 2022)

* Fixes a bug where the report would be empty when pytest-xdist is used [#40](https://github.com/pytest-dev/pytest-nunit/issues/40)

## 1.0.0 (16th March 2022)

* Initial stable v1 release

## 0.6.0 (4th August 2020)

* fix unicode escapes in cdata (#39)
* fix start/stop time calculation (#42)
* dropping support for python3.4 (#45)
* dropping support for old xdist versions (#44)

## 0.5.3 (15th April 2020)

* Bugfix - Fix time taken for tests under certain scenarios causing crash on pytest_sessionfinish

## 0.5.2 (30th August 2019)

* Bugfix - Escape tabbed unicode characters from stdout feed from being in CDATA output

## 0.5.1 (30th August 2019)

* Bugfix - Fixed cause of crash for tests that could be discovered but never executed

## 0.5.0 (30th August 2019)

* Docstrings of nodes (functions) are set as the label for TestCase elements (contribution by @mikeattara)
* Pytest -k keyword filters are added to the test run filter element under ``name``.
* Pytest -m marker filters are added to the test run filter element under ``namespace``.
* Any path filters are added to the test run filter element under ``test``.
* Each Python module containing tests is now a separate ``test-suite`` element, instead of having one large suite
* Docstrings of modules are set as the label for TestSuite elements

## 0.4.0 (28th August 2019)

* Added user domain (contribution by @williano)
* Added tests and help for xdist execution (contribution by @mei-li)
* Dynamically use the keyword list when generating schema to avoid reserved word collision (contribution by @gerhardtdatsomor)
* Add method names, classnames and module names to output (contribution by @adekanyetomie)
* Added locale and uiculture properties to runtime output (contribution by @terrameijar)
* Added ``nunit_attach_on`` INI option to control when attachments are included in test cases.

## 0.3.0 (15th July 2019)

* Added ``--nunit-prefix`` option.

## 0.2.1 (15th July 2019)

* First stable release
