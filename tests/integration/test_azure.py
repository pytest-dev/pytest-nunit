"""
Test things in Azure Pipelines
"""

import os
import pytest

def test_attachment(add_nunit_attachment):
    """
    Test adding custom attachment
    """
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixture.gif')
    add_nunit_attachment(path, "PBJT")
    assert 1 == 1

def test_property(record_nunit_property):
    """
    Test adding custom property
    """
    record_nunit_property("test", "value")
    assert 1 == 1


def test_failure():
    assert 1 == 0


@pytest.mark.skip("Example skip")
def test_skip():
    assert 1 == 0
