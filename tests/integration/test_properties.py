"""
Test adding properties to tests
"""
import xmlschema
import os


def test_basic_property(testdir, tmpdir):
    """
    Test a basic test with an additional property
    """
    testdir.makepyfile("""
        def test_basic(record_nunit_property):
            record_nunit_property("test", "value")
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_basic PASSED*',
    ])
    assert result.ret == 0
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 1, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 0, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 1
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 0
    assert out['test-suite']['@skipped'] == 0
    assert out['test-suite']['test-case']['properties']['property'][1]['@name'] == "test"
    assert out['test-suite']['test-case']['properties']['property'][1]['@value'] == "value"


def test_attachment(testdir, tmpdir):
    """
    Test a basic test with an additional property
    """
    testdir.makepyfile("""
        def test_basic(add_nunit_attachment):
            add_nunit_attachment("file.pth", "desc")
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_basic PASSED*',
    ])
    assert result.ret == 0
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 1, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 0, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 1
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 0
    assert out['test-suite']['@skipped'] == 0
    assert out['test-suite']['test-case']['attachments']['attachment'][0]['description'] == "desc"
    assert out['test-suite']['test-case']['attachments']['attachment'][0]['filePath'] == "file.pth"
