"""
Test conversion of collected results into module reports.
"""

import pytest

from datetime import datetime, timedelta
from pytest_nunit.plugin import NunitXML

# This class method takes a dict of node_id->dict representing all the
# information we collected in _NunitNodeReporter, and returns a
# ModuleReport (based on all the provided cases)
create_report = NunitXML._create_module_report


def test_empty_report():
    report = create_report({})
    assert 0 == report.duration
    assert {} == report.cases
    assert dict.fromkeys(report.stats, 0) == report.stats


class _TestMaker:
    def __init__(self):
        self.now = datetime.now()

    def __call__(self, outcome, duration=1.0):
        start = self.now
        self.now = stop = start + timedelta(seconds=duration)

        return {
            "outcome": outcome,
            "start": start,
            "stop": stop,
        }


@pytest.fixture()
def make_test():
    return _TestMaker()


def test_simple_report(make_test):
    report = create_report(
        {
            "A": make_test("passed", 1),
            "B": make_test("passed", 8),
            "C": make_test("failed", 4),
            "D": make_test("skipped", 2),
        }
    )
    assert 15 == report.duration
    assert 2 == report.stats["passed"]
    assert 1 == report.stats["failure"]
    assert 1 == report.stats["skipped"]
