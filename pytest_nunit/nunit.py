import sys
from .models import TestRunType, TestResultType, NonnegativeInt32, TestFilterType
from .attrs2xml import AttrsXmlRenderer


class NunitTestRun(object):
    """
    Convert a test report into a Nunit Test Run
    """
    def __init__(self, nunitxml):
        self.nunitxml = nunitxml

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
            filter=TestFilterType())

    def generate_xml(self):
        tr = self.as_test_run()
        return AttrsXmlRenderer.render(tr, 'test-run')
