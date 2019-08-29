"""
Test adding properties to tests
"""
import xmlschema
import os


def test_keyword_filter(testdir, tmpdir):
    testdir.makepyfile("""
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, '-k basic'
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

    assert 'filter' in out
    assert out['filter']['name'][0]['$'] == 'basic'
    assert out['filter']['name'][0]['@re'] == 0


def test_keyword_filter_complex(testdir, tmpdir):
    testdir.makepyfile("""
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, '-k "test or basic"'
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

    assert 'filter' in out
    assert out['filter']['name'][0]['$'] == '"test or basic"'
    assert out['filter']['name'][0]['@re'] == 0


def test_marker_filter(testdir, tmpdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.foo
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, '-m foo'
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

    assert 'filter' in out
    assert out['filter']['namespace'][0]['$'] == 'foo'
    assert out['filter']['namespace'][0]['@re'] == 0


def test_marker_filter_complex(testdir, tmpdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.baz
        @pytest.mark.foo
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, '-m "foo or baz"'
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

    assert 'filter' in out
    assert out['filter']['namespace'][0]['$'] == '"foo or baz"'
    assert out['filter']['namespace'][0]['@re'] == 0


def test_path_filter(testdir, tmpdir):
    testdir.makepyfile("""
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)
    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, 'test_path_filter.py'
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

    assert 'filter' in out
    assert out['filter']['test'][0]['$'] == 'test_path_filter.py'
    assert out['filter']['test'][0]['@re'] == 0


def test_path_filter_complex(testdir, tmpdir):
    testdir.makepyfile("""
        def test_basic(record_nunit_property):
            assert 1 == 1
    """)

    outfile = tmpdir.join('out.xml')
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile_pth, 'test_path_filter_complex.py', '.'
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

    assert 'filter' in out
    assert out['filter']['test'][0]['$'] == 'test_path_filter.py'
    assert out['filter']['test'][0]['@re'] == 0

    assert out['filter']['test'][1]['$'] == 'test_path_filter.py'
    assert out['filter']['test'][1]['@re'] == 0
