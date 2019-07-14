"""
Test things in Azure Pipelines
"""

def test_attachment(add_nunit_attachment):
    pth = os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
    add_nunit_attachment(path, "PBJT")
    assert 1 == 1