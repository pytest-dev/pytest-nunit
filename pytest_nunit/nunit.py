import sys
from .models import (TestRunType, TestResultType, TestCaseElementType, TestSuiteElementType, TestStatusType, TestRunStateType, TestSuiteTypeType)
from .attrs2xml import AttrsXmlRenderer


class NunitTestRun(object):
    """
    Convert a test report into a Nunit Test Run
    """
    def __init__(self, nunitxml):
        self.nunitxml = nunitxml

    @property
    def test_cases(self):
        return [TestCaseElementType(
            id_="test_case",
            )
        ]

    @property
    def test_suites(self):
        return [
            TestSuiteElementType(
                id_="",
                name="example",
                fullname="example",
                methodname="test",
                classname="testClass",
                test_suite=None,
                test_case=None,
                runstate=TestRunStateType.Runnable,
                type_=TestSuiteTypeType.TestSuite,
                testcasecount=0,
                result=TestStatusType.Passed,
                label="",
                site=None,
                start_time=0,
                end_time=0,
                duration=0,
                asserts=0,
                total=0,
                passed=0,
                failed=0,
                warnings=0,
                inconclusive=0,
                skipped=0
            )
        ]

    def as_test_run(self):
        return TestRunType(
            id_="2",
            name=self.nunitxml.suite_name,
            fullname="",
            testcasecount=0,
            result=TestResultType.Passed,
            label="",
            start_time=0.0,
            end_time=0.0,
            duration=0.0,
            total=1,
            passed=1,
            failed=1,
            inconclusive=1,
            skipped=1,
            asserts=1,
            random_seed=sys.flags.hash_randomization,
            command_line=' '.join(sys.argv),
            filter=None,
            test_case=None,
            test_suite=self.test_suites)

    def generate_xml(self):
        tr = self.as_test_run()
        return AttrsXmlRenderer.render(tr, 'test-run')
