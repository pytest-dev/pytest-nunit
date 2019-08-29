import os
import xmlschema


def test_prefix(testdir, tmpdir):
    """
    Test that prefixes are set on the suite name
    """
    testdir.makepyfile(
        """
        def test_basic():
            assert 1 == 1
    """
    )
    outfile = tmpdir.join("out.xml")
    outfile_pth = str(outfile)

    result = testdir.runpytest(
        "-v", "--nunit-xml=" + outfile_pth, "--nunit-prefix=test1."
    )
    result.stdout.fnmatch_lines(["*test_basic PASSED*"])
    assert result.ret == 0
    os.path.exists(outfile_pth)
    xs = xmlschema.XMLSchema(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "../../ext/nunit-src/TestResult.xsd",
        ),
        validation="lax",
    )
    out = xs.to_dict(outfile_pth)
    assert out["@total"] == 1, out
    assert out["@passed"] == 1, out
    assert out["@failed"] == 0, out
    assert out["@skipped"] == 0, out
    assert out["test-suite"]["@total"] == 1
    assert out["test-suite"]["@passed"] == 1
    assert out["test-suite"]["@failed"] == 0
    assert out["test-suite"]["@skipped"] == 0
    assert out["test-suite"]["test-case"]["@name"] == "test1.test_prefix.py::test_basic"
