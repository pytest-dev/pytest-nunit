import sys
from .models import (TestRunType, TestResultType, TestCaseElementType, TestSuiteElementType, TestStatusType, TestRunStateType, TestSuiteTypeType, PropertyBagType, PropertyType)
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
            id_=nodeid,
            name=nodeid, 
            fullname=nodeid, 
            methodname=case['report'].head_line,
            properties=PropertyBagType(property=[PropertyType(name="test_property", value="test value")]), 
            environment=None, 
            settings=None, 
            failure=None, 
            reason=None, 
            output='test output',
            assertions=None,
            classname="TestFoo", 
            runstate=TestRunStateType.Runnable, 
            seed=str(sys.flags.hash_randomization), 
            result=TestStatusType.Passed, # TODO 
            label="test_label", 
            site=None, 
            start_time=case['start'], 
            end_time=case['stop'], 
            duration=case['duration'], 
            asserts=0
            )
            for nodeid, case in self.nunitxml.cases.items()
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
                properties=PropertyBagType(property=[PropertyType(name="test_property", value="test value")]), 
                environment=None, 
                settings=None, 
                failure=None, 
                reason=None, 
                output='test output',
                assertions=None,
                test_case=self.test_cases,
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
