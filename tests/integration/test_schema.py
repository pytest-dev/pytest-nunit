"""
Validate the output XML file against the schema
"""
import os
import xmlschema
from xml.etree import ElementTree


def test_basic_schema(testdir, tmpdir):
    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_basic():
            assert 1 == 1
    """)
    outfile=os.path.join(tmpdir, 'out.xml')

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_basic PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

    # ensure the output file exists
    os.path.exists(outfile)

    xs = xmlschema.XMLSchema('/Users/anthonyshaw/PycharmProjects/pytest-nunit/ext/TestResult.xsd')  # TODO: !!!!
    xt = ElementTree.parse(outfile)
    assert xs.is_valid(xt), xs.validate(xt)