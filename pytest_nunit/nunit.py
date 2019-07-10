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
                id_="2",
                name=self.nunitxml.suite_name,
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
                start_time=self.nunitxml.suite_start_time,
                end_time=self.nunitxml.suite_stop_time,
                duration=self.nunitxml.suite_time_delta,
                asserts=self.nunitxml.stats['asserts'],
                total=self.nunitxml.stats['total'],
                passed=self.nunitxml.stats['passed'],
                failed=self.nunitxml.stats['failure'],
                warnings=0,
                inconclusive=0,
                skipped=self.nunitxml.stats['skipped']
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
            start_time=self.nunitxml.suite_start_time,
            end_time=self.nunitxml.suite_stop_time,
            duration=self.nunitxml.suite_time_delta,
            total=self.nunitxml.stats['total'],
            passed=self.nunitxml.stats['passed'],
            failed=self.nunitxml.stats['failure'],
            inconclusive=0,
            skipped=self.nunitxml.stats['skipped'],
            asserts=self.nunitxml.stats['asserts'],
            random_seed=sys.flags.hash_randomization,
            command_line=' '.join(sys.argv),
            filter=None,
            test_case=None,
            test_suite=self.test_suites)

    def generate_xml(self):
        tr = self.as_test_run()
        return AttrsXmlRenderer.render(tr, 'test-run')
