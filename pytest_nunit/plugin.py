"""
Nunit plugin for pytest

Based (loosely) on the Junit XML output.

Shares the same pattern of CLI options for ease of use.
"""
from _pytest.config import filename_arg

import os
import time
import functools

from .nunit import NunitTestRun


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--nunitxml",
        "--nunit-xml",
        action="store",
        dest="nunit_xmlpath",
        metavar="path",
        type=functools.partial(filename_arg, optname="--nunitxml"),
        default=None,
        help="create nunit-xml style report file at given path.",
    )
    group.addoption(
        "--nunitprefix",
        "--nunit-prefix",
        action="store",
        metavar="str",
        default=None,
        help="prepend prefix to classnames in nunit-xml output",
    )
    parser.addini(
        "nunit_suite_name", "Test suite name for NUnit report", default="pytest"
    )
    parser.addini(
        "nunit_logging",
        "Write captured log messages to NUnit report: "
        "one of no|system-out|system-err",
        default="no",
    )  # choices=['no', 'stdout', 'stderr'])
    parser.addini(
        "nunit_log_passing_tests",
        "Capture log information for passing tests to NUnit report: ",
        type="bool",
        default=True,
    )
    parser.addini(
        "nunit_duration_report",
        "Duration time to report: one of total|call",
        default="total",
    )  # choices=['total', 'call'])


def pytest_configure(config):
    nunit_xmlpath = config.option.nunit_xmlpath
    # prevent opening xmllog on slave nodes (xdist)
    if nunit_xmlpath and not hasattr(config, "slaveinput"):
        config._nunitxml = NunitXML(
            nunit_xmlpath,
            config.option.nunitprefix,
            config.getini("nunit_suite_name"),
            config.getini("nunit_logging"),
            config.getini("nunit_duration_report"),
            config.getini("nunit_log_passing_tests"),
        )
        config.pluginmanager.register(config._nunitxml)


def pytest_unconfigure(config):
    nunitxml = getattr(config, "_nunitxml", None)
    if nunitxml:
        del config._nunitxml
        config.pluginmanager.unregister(nunitxml)


class _NunitNodeReporter:
    def __init__(self, nodeid, nunit_xml):
        self.id = nodeid
        self.nunit_xml = nunit_xml
        self.duration = 0.0

    def append(self, node):
        self.nunit_xml.add_stats(type(node).__name__)
        self.nodes.append(node)

    def record_testreport(self, testreport):
        pass

    def write_captured_output(self, report):
        if not self.nunit_xml.log_passing_tests and report.passed:
            return

        content_out = report.capstdout
        content_log = report.caplog
        content_err = report.capstderr

    def append_pass(self, report):
        pass

    def append_failure(self, report):
        pass

    def append_collect_error(self, report):
        pass

    def append_collect_skipped(self, report):
        pass

    def append_error(self, report):
        pass

    def append_skipped(self, report):
        pass

    def finalize(self):
        pass


class NunitXML:
    def __init__(
        self,
        logfile,
        prefix,
        suite_name="pytest",
        logging="no",
        report_duration="total",
        log_passing_tests=True,
    ):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.prefix = prefix
        self.suite_name = suite_name
        self.logging = logging
        self.log_passing_tests = log_passing_tests
        self.report_duration = report_duration
        self.stats = dict.fromkeys(["error", "passed", "failure", "skipped"], 0)
        self.node_reporters = {}  # nodeid -> _NodeReporter
        self.node_reporters_ordered = []
        self.global_properties = []

        # List of reports that failed on call but teardown is pending.
        self.open_reports = []
        self.cnt_double_fail_tests = 0

    def finalize(self, report):
        nodeid = getattr(report, "nodeid", report)
        # local hack to handle xdist report order
        slavenode = getattr(report, "node", None)
        reporter = self.node_reporters.pop((nodeid, slavenode))
        if reporter is not None:
            reporter.finalize()

    def node_reporter(self, report):
        nodeid = getattr(report, "nodeid", report)
        # local hack to handle xdist report order
        slavenode = getattr(report, "node", None)

        key = nodeid, slavenode

        if key in self.node_reporters:
            # TODO: breaks for --dist=each
            return self.node_reporters[key]

        reporter = _NunitNodeReporter(nodeid, self)

        self.node_reporters[key] = reporter
        self.node_reporters_ordered.append(reporter)

        return reporter

    def _opentestcase(self, report):
        reporter = self.node_reporter(report)
        reporter.record_testreport(report)
        return reporter

    def pytest_runtest_logreport(self, report):
        """handle a setup/call/teardown report, generating the appropriate
        xml tags as necessary.
        note: due to plugins like xdist, this hook may be called in interlaced
        order with reports from other nodes. for example:
        usual call order:
            -> setup node1
            -> call node1
            -> teardown node1
            -> setup node2
            -> call node2
            -> teardown node2
        possible call order in xdist:
            -> setup node1
            -> call node1
            -> setup node2
            -> call node2
            -> teardown node2
            -> teardown node1
        """
        close_report = None
        if report.passed:
            if report.when == "call":  # ignore setup/teardown
                reporter = self._opentestcase(report)
                reporter.append_pass(report)
        elif report.failed:
            if report.when == "teardown":
                # The following vars are needed when xdist plugin is used
                report_wid = getattr(report, "worker_id", None)
                report_ii = getattr(report, "item_index", None)
                close_report = next(
                    (
                        rep
                        for rep in self.open_reports
                        if (
                            rep.nodeid == report.nodeid
                            and getattr(rep, "item_index", None) == report_ii
                            and getattr(rep, "worker_id", None) == report_wid
                        )
                    ),
                    None,
                )
                if close_report:
                    # We need to open new testcase in case we have failure in
                    # call and error in teardown in order to follow junit
                    # schema
                    self.finalize(close_report)
                    self.cnt_double_fail_tests += 1
            reporter = self._opentestcase(report)
            if report.when == "call":
                reporter.append_failure(report)
                self.open_reports.append(report)
            else:
                reporter.append_error(report)
        elif report.skipped:
            reporter = self._opentestcase(report)
            reporter.append_skipped(report)
        self.update_testcase_duration(report)
        if report.when == "teardown":
            reporter = self._opentestcase(report)
            reporter.write_captured_output(report)

            for propname, propvalue in report.user_properties:
                reporter.add_property(propname, propvalue)

            self.finalize(report)
            report_wid = getattr(report, "worker_id", None)
            report_ii = getattr(report, "item_index", None)
            close_report = next(
                (
                    rep
                    for rep in self.open_reports
                    if (
                        rep.nodeid == report.nodeid
                        and getattr(rep, "item_index", None) == report_ii
                        and getattr(rep, "worker_id", None) == report_wid
                    )
                ),
                None,
            )
            if close_report:
                self.open_reports.remove(close_report)

    def update_testcase_duration(self, report):
        """accumulates total duration for nodeid from given report and updates
        the Junit.testcase with the new total if already created.
        """
        if self.report_duration == "total" or report.when == self.report_duration:
            reporter = self.node_reporter(report)
            reporter.duration += getattr(report, "duration", 0.0)

    def pytest_collectreport(self, report):
        if not report.passed:
            reporter = self._opentestcase(report)
            if report.failed:
                reporter.append_collect_error(report)
            else:
                reporter.append_collect_skipped(report)

    def pytest_internalerror(self, excrepr):
        reporter = self.node_reporter("internal")

    def pytest_sessionstart(self):
        self.suite_start_time = time.time()

    def pytest_sessionfinish(self):
        dirname = os.path.dirname(os.path.abspath(self.logfile))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        logfile = open(self.logfile, "w", encoding="utf-8")
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time

        numtests = (
            self.stats["passed"]
            + self.stats["failure"]
            + self.stats["skipped"]
            + self.stats["error"]
            - self.cnt_double_fail_tests
        )
        logfile.write('<?xml version="1.0" encoding="utf-8"?>')

        result = NunitTestRun(self).generate_xml()

        logfile.write(result)

        logfile.close()

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", "generated Nunit xml file: %s" % (self.logfile))


