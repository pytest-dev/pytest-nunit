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
    assert out['test-suite']['test-case']['@classname'] == 'test_basic_property.py'
    assert out['test-suite']['test-case']['@methodname'] == 'test_basic'
    


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


def test_attachment_attach_on_any(testdir, tmpdir):
    """
    Test that nunit_attach_on=any sets attachment properties
    """
    testdir.makepyfile("""
        def test_pass(add_nunit_attachment):
            add_nunit_attachment("pass.pth", "desc")
            assert 1 == 1
        def test_fail(add_nunit_attachment):
            add_nunit_attachment("fail.pth", "desc")
            assert 1 == 0

    """)
    testdir.makefile(".ini", pytest="[pytest]\nnunit_attach_on=any\n")
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_pass PASSED*',
        '*test_fail FAILED*',
    ])
    assert result.ret == 1
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 2, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 1, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 2
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 1
    assert out['test-suite']['@skipped'] == 0
    for case in out['test-suite']['test-case']:
        if case['@name'] == 'test_attachment_attach_on_any.py::test_pass':
            assert case['attachments']['attachment'][0]['description'] == "desc"
            assert case['attachments']['attachment'][0]['filePath'] == "pass.pth"
        else:
            assert case['attachments']['attachment'][0]['description'] == "desc"
            assert case['attachments']['attachment'][0]['filePath'] == "fail.pth"


def test_attachment_attach_on_fail(testdir, tmpdir):
    """
    Test that nunit_attach_on=fail sets attachment properties
    """
    testdir.makepyfile("""
        def test_pass(add_nunit_attachment):
            add_nunit_attachment("pass.pth", "desc")
            assert 1 == 1
        def test_fail(add_nunit_attachment):
            add_nunit_attachment("fail.pth", "desc")
            assert 1 == 0

    """)
    testdir.makefile(".ini", pytest="[pytest]\nnunit_attach_on=fail\n")
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_pass PASSED*',
        '*test_fail FAILED*',
    ])
    assert result.ret == 1
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 2, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 1, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 2
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 1
    assert out['test-suite']['@skipped'] == 0
    for case in out['test-suite']['test-case']:
        if case['@name'] == 'test_attachment_attach_on_fail.py::test_fail':
            assert case['attachments']['attachment'][0]['description'] == "desc"
            assert case['attachments']['attachment'][0]['filePath'] == "fail.pth"
        else:
            assert 'attachments' not in case

def test_attachment_attach_on_pass(testdir, tmpdir):
    """
    Test that nunit_attach_on=pass sets attachment properties
    """
    testdir.makepyfile("""
        def test_pass(add_nunit_attachment):
            add_nunit_attachment("pass.pth", "desc")
            assert 1 == 1
        def test_fail(add_nunit_attachment):
            add_nunit_attachment("fail.pth", "desc")
            assert 1 == 0

    """)
    testdir.makefile(".ini", pytest="[pytest]\nnunit_attach_on=pass\n")
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth
    )
    result.stdout.fnmatch_lines([
        '*test_pass PASSED*',
        '*test_fail FAILED*',
    ])
    assert result.ret == 1
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    out = xs.to_dict(outfile_pth)
    assert out['@total'] == 2, out
    assert out['@passed'] == 1, out
    assert out['@failed'] == 1, out
    assert out['@skipped'] == 0, out
    assert out['test-suite']['@total'] == 2
    assert out['test-suite']['@passed'] == 1
    assert out['test-suite']['@failed'] == 1
    assert out['test-suite']['@skipped'] == 0
    for case in out['test-suite']['test-case']:
        if case['@name'] == 'test_attachment_attach_on_pass.py::test_pass':
            assert case['attachments']['attachment'][0]['description'] == "desc"
            assert case['attachments']['attachment'][0]['filePath'] == "pass.pth"
        else:
            assert 'attachments' not in case, case['attachments']


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
    assert '@label' not in out['test-suite']['test-case']
