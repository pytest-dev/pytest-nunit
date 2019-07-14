"""
Test things in Azure Pipelines
"""

import os


def test_attachment(add_nunit_attachment):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
    add_nunit_attachment(path, "PBJT")
    assert 1 == 1