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
    assert "test" in [i['@name'] for i in out['test-suite']['test-case']['properties']['property']]
    assert "value" in [i['@value'] for i in out['test-suite']['test-case']['properties']['property']]


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


def test_slow_test(testdir, tmpdir):
    """
    Test a test that takes 3 seconds
    """
    testdir.makepyfile("""
        import time
        def test_basic():
            time.sleep(3)
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
    assert out['test-suite']['test-case']['@duration'] > 3.0


def test_docstring(testdir, tmpdir):
    testdir.makepyfile("""
        def test_docstring(record_nunit_property):
            '''Hello'''
            record_nunit_property("test", "value")
            assert 1 == 1  
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_docstring PASSED*',
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
    assert out['test-suite']['test-case']['@label'] == "Hello"


def test_no_docstring(testdir, tmpdir):
    testdir.makepyfile("""
        def test_no_docstring(record_nunit_property):
            record_nunit_property("test", "value")
            assert 1 == 1  
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest('-v', '--nunit-xml=' + outfile_pth)
    result.stdout.fnmatch_lines([
        '*test_no_docstring PASSED*',
    ])
    assert result.ret == 0
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '../../ext/nunit-src/TestResult.xsd'),
                             validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 1, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 0, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 1
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 0
    assert out['test-suite']['@skipped'] == 0
    assert out['test-suite']['test-case']['@label'] == ""
