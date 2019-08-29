"""
Test basic situations
"""
import pytest


def test_one_and_one():
    """
    Test 1 + 1
    """
    assert 1 == 1


@pytest.mark.xfail()
def test_one_and_two():
    assert 1 == 2
