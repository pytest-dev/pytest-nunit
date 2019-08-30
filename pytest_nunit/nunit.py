import sys
import os
import locale
import platform
import getpass
from .models.nunit import (
    TestRunType,
    TestResultType,
    TestCaseElementType,
    TestSuiteElementType,
    TestStatusType,
    TestRunStateType,
    TestSuiteTypeType,
    PropertyBagType,
    PropertyType,
    EnvironmentType,
    AttachmentsType,
    AttachmentType,
    ReasonType,
    FailureType,
    TestFilterType,
    ValueMatchFilterType,
)
from .attrs2xml import AttrsXmlRenderer, CdataComment

FRAMEWORK_VERSION = "3.6.2"  # Nunit version this was based on
CLR_VERSION = sys.version


PYTEST_TO_NUNIT = {
    "passed": TestStatusType.Passed,
    "failed": TestStatusType.Failed,
    "skipped": TestStatusType.Skipped,
}


def _get_user_id():
    try:
        username = getpass.getuser()
    except ImportError:  # Windows
        username = "UNKNOWN"

    return (username, platform.node())


def _format_assertions(case):
    # TODO
    return None


def get_node_names(nodeid):
    parts = nodeid.split("::")
    if len(parts) >= 2:
        return tuple(parts[-2:])
    else:
        return ("", "")


def _format_attachments(case, attach_on):
    """
    Format an attachment list for a test case

    :param case: The test case
    :type  case: :class:`pytest.TestCase`
    
    :param attach_on: Attach-on criteria, one of any|pass|fail
    :type  attach_on: ``str``

    :returns: a formatted attachment list
    :rtype: :class:`AttachmentsType`
    """
    if case["attachments"]:
        result = PYTEST_TO_NUNIT.get(case["outcome"], TestStatusType.Inconclusive)
        # Guard clauses
        include_attachments = attach_on == "any"

        if attach_on == "pass" and result == TestStatusType.Passed:
            include_attachments = True
        if attach_on == "fail" and result == TestStatusType.Failed:
            include_attachments = True

        if include_attachments:
            return AttachmentsType(
                attachment=[
                    AttachmentType(filePath=k, description=v)
                    for k, v in case["attachments"].items()
                ]
            )
    return None


def _format_filters(filters_):
    """
    Create a filter list

    :param filters_: The runtime filters
    :type  filters_: `pytest_nunit.plugin.PytestFilter`
    """
    if (
        filters_.keyword is None
        and filters_.file_or_dir is None
        and filters_.markers is None
    ):
        return None

    return TestFilterType(
        test=[ValueMatchFilterType(name=path, re=0) for path in filters_.file_or_dir]
        if filters_.file_or_dir
        else None,
        not_=None,
        and_=None,
        or_=None,
        cat=None,
        class_=None,
        id_=None,
        method=None,
        namespace=ValueMatchFilterType(name=filters_.markers, re=0)
        if filters_.markers
        else None,
        prop=None,
        name=ValueMatchFilterType(name=filters_.keyword, re=0)
        if filters_.keyword
        else None,
    )


def _getlocale():
    language_code = locale.getdefaultlocale()[0]
    if language_code:
        return language_code
    return "en-US"


class NunitTestRun(object):
    """
    Convert a test report into a Nunit Test Run
    """

    def __init__(self, nunitxml):
        self.nunitxml = nunitxml

    @property
    def environment(self):
        return EnvironmentType(
            framework_version=FRAMEWORK_VERSION,
            clr_version=CLR_VERSION,
            os_version=platform.release(),
            platform=platform.system(),
            cwd=os.getcwd(),
            machine_name=platform.machine(),
            user=_get_user_id()[0] if self.nunitxml.show_username else "",
            user_domain=_get_user_id()[1] if self.nunitxml.show_user_domain else "",
            culture=_getlocale(),
            uiculture=_getlocale(),
            os_architecture=platform.architecture()[0],
        )

    def test_cases(self, module):
        return [
            TestCaseElementType(
                id_=str(case["idref"]),
                name=case["name"],
                fullname=nodeid,
                methodname=get_node_names(nodeid)[1],
                properties=PropertyBagType(
                    property=[
                        PropertyType(name=k, value=v)
                        for k, v in case["properties"].items()
                    ]
                ),
                environment=self.environment,
                settings=None,  # TODO : Add settings as optional fixture
                failure=FailureType(
                    message=CdataComment(text=case["error"]),
                    stack_trace=CdataComment(text=case["stack-trace"]),
                ),
                reason=ReasonType(message=CdataComment(text=case["reason"])),
                output=CdataComment(text=case["reason"]),
                assertions=_format_assertions(case),
                attachments=_format_attachments(case, self.nunitxml.attach_on),
                classname=get_node_names(nodeid)[0],
                runstate=TestRunStateType.Skipped
                if case["outcome"] == "skipped"
                else TestRunStateType.Runnable,
                seed=str(sys.flags.hash_randomization),
                result=PYTEST_TO_NUNIT.get(
                    case["outcome"], TestStatusType.Inconclusive
                ),
                label=self.nunitxml.node_descriptions[nodeid],
                site=None,
                start_time=case["start"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                end_time=case["stop"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                duration=case["duration"],
                asserts=0,  # TODO : Add assert count
            )
            for nodeid, case in self.nunitxml.modules[module].cases.items()
        ]

    @property
    def test_suites(self):
        return [
            TestSuiteElementType(
                id_=nodeid,
                name=nodeid,
                fullname=nodeid,
                methodname="",
                classname="",
                test_suite=None,
                properties=PropertyBagType(
                    property=[PropertyType(name="python_version", value=sys.version)]
                ),
                environment=self.environment,
                settings=None,
                failure=None,
                reason=None,
                output=None,
                assertions=None,
                attachments=None,
                test_case=self.test_cases(nodeid),
                runstate=TestRunStateType.Runnable,
                type_=TestSuiteTypeType.Assembly,
                testcasecount=module.stats["total"],
                result=TestStatusType.Passed,  # TODO: Determine suite status
                label=self.nunitxml.module_descriptions[nodeid],
                site=None,
                start_time=module.start.strftime("%Y-%m-%d %H:%M:%S.%f"),
                end_time=module.stop.strftime("%Y-%m-%d %H:%M:%S.%f"),
                duration=module.duration,
                asserts=module.stats["asserts"],
                total=module.stats["total"],
                passed=module.stats["passed"],
                failed=module.stats["failure"],
                warnings=0,
                inconclusive=0,
                skipped=module.stats["skipped"],
            )
            for nodeid, module in self.nunitxml.modules.items()
        ]

    def as_test_run(self):
        return TestRunType(
            id_="2",
            testcasecount=self.nunitxml.stats["total"],
            result=TestResultType.Passed,
            start_time=self.nunitxml.suite_start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            end_time=self.nunitxml.suite_stop_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            duration=int(self.nunitxml.suite_time_delta),
            total=self.nunitxml.stats["total"],
            passed=self.nunitxml.stats["passed"],
            failed=self.nunitxml.stats["failure"],
            inconclusive=0,
            skipped=self.nunitxml.stats["skipped"],
            asserts=self.nunitxml.stats["asserts"],
            command_line=" ".join(sys.argv),
            filter_=_format_filters(self.nunitxml.filters),
            test_case=None,
            test_suite=self.test_suites,
            engine_version=FRAMEWORK_VERSION,
            clr_version=CLR_VERSION,
        )

    def generate_xml(self):
        tr = self.as_test_run()
        return AttrsXmlRenderer.render(tr, "test-run")
