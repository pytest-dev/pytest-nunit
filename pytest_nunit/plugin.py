"""
Nunit plugin for pytest

Based (loosely) on the Junit XML output.

Shares the same pattern of CLI options for ease of use.
"""
from _pytest.config import filename_arg

from io import open
import os
import sys
from datetime import datetime
import functools
from collections import namedtuple, defaultdict, Counter

from .nunit import NunitTestRun

import logging
import pytest

logging.basicConfig()
log = logging.getLogger("__name__")


PytestFilters = namedtuple("PytestFilters", "keyword markers file_or_dir")
ModuleReport = namedtuple("ModuleReport", "stats cases start stop duration")
ParentlessNode = "PARENTLESS_NODE"

if sys.version_info < (3,):
    def min_with_default(seq, default):
        try:
            return min(seq)
        except ValueError:
            return default

    def max_with_default(seq, default):
        try:
            return max(seq)
        except ValueError:
            return default
else:
    min_with_default = min
    max_with_default = max


def pytest_addoption(parser):
    """Allow export settings on CLI."""
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
        default="",
        help="prepend prefix to classnames in nunit-xml output",
    )
    parser.addini(
        "nunit_suite_name", "Test suite name for NUnit report", default="pytest"
    )
    parser.addini(
        "nunit_show_username", "Display username in results", "bool", default=False
    )

    parser.addini(
        "nunit_show_user_domain",
        "Display computer domain in results",
        "bool",
        default=False,
    )

    parser.addini(
        "nunit_attach_on",
        "Set test attachments for certain test results: " "one of any|pass|fail",
        default="any",
    )  # choices=['any', 'pass', 'fail'])


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """
    Configure XML export paths and settings.
    """
    nunit_xmlpath = config.option.nunit_xmlpath

    # prevent opening xmllog on worker nodes (xdist)
    if nunit_xmlpath and not hasattr(config, "workerinput"):

        filters = PytestFilters(
            keyword=config.known_args_namespace.keyword.strip(),
            markers=config.known_args_namespace.markexpr.strip(),
            file_or_dir=config.known_args_namespace.file_or_dir,
        )

        config._nunitxml = NunitXML(
            logfile=nunit_xmlpath,
            prefix=config.option.nunitprefix,
            suite_name=config.getini("nunit_suite_name"),
            show_username=config.getini("nunit_show_username"),
            show_user_domain=config.getini("nunit_show_user_domain"),
            attach_on=config.getini("nunit_attach_on"),
            filters=filters,
        )
        config.pluginmanager.register(config._nunitxml)


def pytest_unconfigure(config):
    """Unregister plugin and settings."""
    nunitxml = getattr(config, "_nunitxml", None)
    if nunitxml:
        del config._nunitxml
        config.pluginmanager.unregister(nunitxml)


class _NunitNodeReporter:
    def __init__(self, nodeid, nunit_xml):
        self.id = nodeid
        self.nunit_xml = nunit_xml

    def record_testreport(self, testreport):
        """Export to XML."""
        log.debug("record_test_report:{0}".format(testreport))

        if testreport.when == "setup":
            r = self.nunit_xml.cases[testreport.nodeid] = {
                "setup-report": testreport,
                "call-report": None,
                "teardown-report": None,
                "idref": self.nunit_xml.idrefindex,
                "path": testreport.fspath,
                "properties": {
                    "python-version": sys.version,
                    "fspath": testreport.fspath,
                },
                "attachments": None,
                "error": "",
                "stack-trace": "",
                "name": self.nunit_xml.prefix + testreport.nodeid,
            }
            self.nunit_xml.idrefindex += 1  # Inc. node id ref counter
            r["start"] = datetime.utcnow()  # Will be overridden if called
            if testreport.outcome == "skipped":
                log.debug("skipping : {0}".format(testreport.longrepr))
                if isinstance(testreport.longrepr, tuple) and len(testreport.longrepr) > 2:
                    r["error"] = testreport.longrepr[2]
                    r["stack-trace"] = "{0}::{1}".format(
                        testreport.longrepr[0], testreport.longrepr[1]
                    )
                elif hasattr(testreport.longrepr, "traceback"): # Catches internal ExceptionInfo type
                    r["error"] = str(testreport.longrepr)
                    r["stack-trace"] = str(testreport.longrepr.traceback)
                else:
                    r["error"] = testreport.longrepr
        elif testreport.when == "call":
            r = self.nunit_xml.cases[testreport.nodeid]
            r["call-report"] = testreport
            r["error"] = testreport.longreprtext
            r["stack-trace"] = self.nunit_xml._getcrashline(testreport)
        elif testreport.when == "teardown":
            r = self.nunit_xml.cases[testreport.nodeid]
            r["stop"] = datetime.utcnow()
            r["duration"] = (
                (r["stop"] - r["start"]).total_seconds() if r["call-report"] else 0
            )  # skipped.
            r["teardown-report"] = testreport

            if r["setup-report"].outcome == "skipped":
                r["outcome"] = "skipped"
            elif r["setup-report"].outcome == "failed":
                r["outcome"] = "failed"
            elif "failed" in [r["call-report"].outcome, testreport.outcome]:
                r["outcome"] = "failed"
            else:
                r["outcome"] = "passed"
            r["stdout"] = testreport.capstdout
            r["stderr"] = testreport.capstderr
            r["reason"] = testreport.caplog
        else:
            log.debug(testreport)

    def add_property(self, name, value):
        """Add custom property."""
        r = self.nunit_xml.cases[self.id]
        r["properties"][name] = value

    def add_attachment(self, file, description):
        """Add test attachment."""
        r = self.nunit_xml.cases[self.id]
        if r["attachments"] is None:
            r["attachments"] = {}
        r["attachments"][file] = description

    def finalize(self):
        """Capture finalize stage (required)."""
        log.debug("finalize")


@pytest.fixture
def record_nunit_property(request):
    """
    Add extra properties in the Nunit output for the calling test
    """
    # Declare noop
    def add_attr_noop(name, value):
        pass

    attr_func = add_attr_noop

    nunitxml = getattr(request.config, "_nunitxml", None)
    if nunitxml is not None:
        node_reporter = nunitxml.node_reporter(request.node.nodeid)
        attr_func = node_reporter.add_property

    return attr_func


@pytest.fixture
def add_nunit_attachment(request):
    """
    Add an attachment in Nunit output for the calling test
    """
    # Declare noop
    def add_attachment_noop(file, description):
        pass

    attr_func = add_attachment_noop

    nunitxml = getattr(request.config, "_nunitxml", None)
    if nunitxml is not None:
        node_reporter = nunitxml.node_reporter(request.node.nodeid)
        attr_func = node_reporter.add_attachment

    return attr_func


class NunitXML:
    """NUnit XML exporter."""

    def __init__(
        self,
        logfile,
        prefix,
        suite_name="pytest",
        show_username=False,
        show_user_domain=False,
        attach_on="any",
        filters=None,
    ):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.prefix = prefix
        self.suite_name = suite_name
        self.stats = dict.fromkeys(
            ["error", "passed", "failure", "skipped", "total", "asserts"], 0
        )
        self.node_reporters = {}  # nodeid -> _NodeReporter
        self.node_reporters_ordered = []
        self.cases = dict()
        self.show_username = show_username
        self.show_user_domain = show_user_domain
        self.attach_on = attach_on
        logging.debug("Attach on criteria : {0}".format(attach_on))
        self.idrefindex = 100  # Create a unique ID counter
        self.filters = filters

        self.node_descriptions = defaultdict(str)
        self.module_descriptions = defaultdict(str)
        self.node_to_module_map = {}
        self.modules = {}

    def finalize(self, report):
        """Finalize report (required.)"""
        nodeid = getattr(report, "nodeid", report)
        # local hack to handle xdist report order
        workernode = getattr(report, "node", None)
        reporter = self.node_reporters.pop((nodeid, workernode))
        if reporter is not None:
            reporter.finalize()

    def node_reporter(self, report):
        """Report node result."""
        nodeid = getattr(report, "nodeid", report)
        # local hack to handle xdist report order
        workernode = getattr(report, "node", None)

        key = nodeid, workernode

        if key in self.node_reporters:
            # TODO: breaks for --dist=each
            return self.node_reporters[key]

        reporter = _NunitNodeReporter(nodeid, self)

        self.node_reporters[key] = reporter
        self.node_reporters_ordered.append(reporter)

        return reporter

    def pytest_runtest_logreport(self, report):
        """Get Log report."""
        reporter = self.node_reporter(report)
        reporter.record_testreport(report)
        return reporter

    def update_testcase_duration(self, report):
        """Set test case duration time."""
        reporter = self.node_reporter(report)
        reporter.duration += getattr(report, "duration", 0.0)

    def pytest_internalerror(self, excrepr):
        """Capture PyTest failures."""
        reporter = self.node_reporter("internal")
        # TODO: Mark tests as failed and produce stack

    def pytest_sessionstart(self, *args):
        """Mark test session start time."""
        self.suite_start_time = datetime.utcnow()

    def _getcrashline(self, rep):
        try:
            return str(rep.longrepr.reprcrash)
        except AttributeError:
            try:
                return str(rep.longrepr)[:50]
            except AttributeError:
                return ""

    def pytest_collection_modifyitems(self, session, config, items, *args):
        """Map items and test cases to make the XML output easier to read."""
        for item in items:
            if item.parent and hasattr(item.parent, "obj") and item.parent.obj:
                doc = item.parent.obj.__doc__.strip() if item.parent.obj.__doc__ else ""
                self.module_descriptions[item.parent.nodeid] = doc
            if hasattr(item, "obj") and item.obj:
                doc = item.obj.__doc__.strip() if item.obj.__doc__ else ""
                self.node_descriptions[item.nodeid] = doc

            if item.parent:
                self.node_to_module_map[item.nodeid] = item.parent.nodeid
            else:  # A parent-less node could happen with some custom test-collection plugins.
                self.node_to_module_map[item.nodeid] = ParentlessNode

    @classmethod
    def _create_module_report(cls, cases):
        """
        Produces a report with stats and timing information.

        *cases* is a dict of dicts with all the recorded data. Keys are not
        relevant to this method, but will be retained in the cases attribute
        of the returned object.
        """
        stats = dict.fromkeys(
            ["error", "passed", "failure", "skipped", "total", "asserts"], 0
        )
        stats["total"] = len(cases)
        outcomes = Counter(case.get("outcome") for case in cases.values())
        stats["passed"] = outcomes.get("passed", 0)
        stats["failure"] = outcomes.get("failed", 0)
        stats["skipped"] = outcomes.get("skipped", 0)
        start = min_with_default(
            [case["start"] for case in cases.values() if "start" in case], default=datetime.min
        )
        stop = max_with_default(
            [case["stop"] for case in cases.values() if "stop" in case], default=datetime.min
        )
        duration = (stop - start).total_seconds()
        return ModuleReport(
            stats=stats, cases=cases, start=start, stop=stop, duration=duration
        )

    def pytest_sessionfinish(self, session, *args):
        """Wrap up test report and build output file."""
        dirname = os.path.dirname(os.path.abspath(self.logfile))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        self.suite_stop_time = datetime.utcnow()
        self.suite_time_delta = (
            self.suite_stop_time - self.suite_start_time
        ).total_seconds()

        full_report = self._create_module_report(self.cases)
        self.stats.update(full_report.stats)

        # Sort nodes into modules
        for module_id in set(self.node_to_module_map.values()):
            cases = {
                nodeid: self.cases[nodeid]
                for nodeid, m_id in self.node_to_module_map.items()
                if module_id == m_id and nodeid in self.cases
            }
            self.modules[module_id] = self._create_module_report(cases)

        with open(self.logfile, "w", encoding="utf-8") as logfile:
            result = NunitTestRun(self).generate_xml()
            logfile.write(result.decode(encoding="utf-8"))

    def pytest_terminal_summary(self, terminalreporter):
        """Notify XML report path."""
        terminalreporter.write_sep("-", "generated Nunit xml file: %s" % (self.logfile))
