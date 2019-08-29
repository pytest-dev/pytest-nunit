"""
Validate the output XML file against the schema
"""
import os
import xmlschema
from xml.etree import ElementTree


def test_basic_against_reference_schema(testdir, tmpdir):
    """
    Test a basic output against the schema in the Nunit3 source
    """
    # create a temporary pytest test module
    testdir.makepyfile(
        """
        def test_basic():
            assert 1 == 1
    """
    )
    outfile = tmpdir.join("out.xml")
    outfile_pth = str(outfile)

    # run pytest with the following cmd args
    result = testdir.runpytest("-v", "--nunit-xml=" + outfile_pth)

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*test_basic PASSED*"])

    # ensure the output file exists
    os.path.exists(outfile_pth)

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

    my_path = os.path.abspath(os.path.dirname(__file__))
    xs = xmlschema.XMLSchema(
        os.path.join(my_path, "../../ext/nunit-src/TestResult.xsd"), validation="lax"
    )
    xt = ElementTree.parse(outfile_pth)
    assert xs.is_valid(xt), xs.validate(xt)
