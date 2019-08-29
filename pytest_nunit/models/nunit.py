import attr
import enum


class TestDurationType(float):
    pass


class TestResultType(enum.Enum):
    Inconclusive = "Inconclusive"
    Skipped = "Skipped"
    Passed = "Passed"
    Warning = "Warning"
    Failed = "Failed"


class FailureSiteType(enum.Enum):
    Test = "Test"
    SetUp = "SetUp"
    TearDown = "TearDown"
    Parent = "Parent"
    Child = "Child"


class TestStatusType(enum.Enum):
    Inconclusive = "Inconclusive"
    Skipped = "Skipped"
    Passed = "Passed"
    Warning = "Warning"
    Failed = "Failed"


class AssertionStatusType(enum.Enum):
    Inconclusive = "Inconclusive"
    Passed = "Passed"
    Warning = "Warning"
    Failed = "Failed"
    Error = "Error"


class NonnegativeInt32(int):
    pass


class TestRunStateType(enum.Enum):
    NotRunnable = "NotRunnable"
    Runnable = "Runnable"
    Explicit = "Explicit"
    Skipped = "Skipped"
    Ignored = "Ignored"


class TestSuiteTypeType(enum.Enum):
    GenericFixture = "GenericFixture"
    ParameterizedFixture = "ParameterizedFixture"
    Theory = "Theory"
    GenericMethod = "GenericMethod"
    ParameterizedMethod = "ParameterizedMethod"
    Assembly = "Assembly"
    SetUpFixture = "SetUpFixture"
    TestFixture = "TestFixture"
    TestMethod = "TestMethod"
    TestSuite = "TestSuite"


@attr.s
class SettingsType(object):
    setting = attr.ib(
        metadata={"name": "setting", "type": "element", "optional": True},
        type="SettingType",
        default=attr.NOTHING,
    )


@attr.s
class KeyValuePairType(object):
    key = attr.ib(
        metadata={"name": "key", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    value = attr.ib(
        metadata={"name": "value", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )


@attr.s
class SettingType(object):
    item = attr.ib(
        metadata={"name": "item", "type": "element", "optional": True},
        type="KeyValuePairType",
        default=attr.NOTHING,
    )
    name = attr.ib(
        metadata={"name": "name", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    value = attr.ib(
        metadata={"name": "value", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )


@attr.s
class EnvironmentType(object):
    framework_version = attr.ib(
        metadata={"name": "framework-version", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    clr_version = attr.ib(
        metadata={"name": "clr-version", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    os_version = attr.ib(
        metadata={"name": "os-version", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    platform = attr.ib(
        metadata={"name": "platform", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    cwd = attr.ib(
        metadata={"name": "cwd", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    machine_name = attr.ib(
        metadata={"name": "machine-name", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    user = attr.ib(
        metadata={"name": "user", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    user_domain = attr.ib(
        metadata={"name": "user-domain", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    culture = attr.ib(
        metadata={"name": "culture", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    uiculture = attr.ib(
        metadata={"name": "uiculture", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    os_architecture = attr.ib(
        metadata={"name": "os-architecture", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )


@attr.s
class TestRunType(object):
    command_line = attr.ib(
        metadata={"name": "command-line", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    filter_ = attr.ib(
        metadata={"name": "filter", "type": "element", "optional": False},
        type="TestFilterType",
    )
    test_suite = attr.ib(
        metadata={"name": "test-suite", "type": "element", "optional": True},
        type="TestSuiteElementType",
        default=attr.NOTHING,
    )
    test_case = attr.ib(
        metadata={"name": "test-case", "type": "element", "optional": True},
        type="TestCaseElementType",
        default=attr.NOTHING,
    )
    id_ = attr.ib(
        metadata={"name": "id", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    testcasecount = attr.ib(
        metadata={"name": "testcasecount", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    result = attr.ib(
        metadata={"name": "result", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestResultType),
    )
    start_time = attr.ib(
        metadata={"name": "start-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    end_time = attr.ib(
        metadata={"name": "end-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    duration = attr.ib(
        metadata={"name": "duration", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )
    total = attr.ib(
        metadata={"name": "total", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    passed = attr.ib(
        metadata={"name": "passed", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    failed = attr.ib(
        metadata={"name": "failed", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    inconclusive = attr.ib(
        metadata={"name": "inconclusive", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    skipped = attr.ib(
        metadata={"name": "skipped", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    asserts = attr.ib(
        metadata={"name": "asserts", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    clr_version = attr.ib(
        metadata={"name": "clr-version", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    engine_version = attr.ib(
        metadata={"name": "engine-version", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )


@attr.s
class ReasonType(object):
    message = attr.ib(
        metadata={"name": "message", "type": "element", "optional": False}, type=str
    )


@attr.s
class AssertionType(object):
    message = attr.ib(
        metadata={"name": "message", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    stack_trace = attr.ib(
        metadata={"name": "stack-trace", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    result = attr.ib(
        metadata={"name": "result", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )


@attr.s
class AttachmentType(object):
    filePath = attr.ib(
        metadata={"name": "filePath", "type": "element", "optional": False}, type=str
    )
    description = attr.ib(
        metadata={"name": "description", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )


@attr.s
class AttachmentsType(object):
    attachment = attr.ib(
        metadata={"name": "attachment", "type": "element", "optional": False},
        type="AttachmentType",
    )


@attr.s
class AssertionsType(object):
    assertion = attr.ib(
        metadata={"name": "assertion", "type": "element", "optional": False},
        type="AssertionType",
    )


@attr.s
class FailureType(object):
    message = attr.ib(
        metadata={"name": "message", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    stack_trace = attr.ib(
        metadata={"name": "stack-trace", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )


@attr.s
class TestFilterType(object):
    not_ = attr.ib(
        metadata={"name": "not", "type": "element", "optional": True},
        type="None",
        default=attr.NOTHING,
    )
    and_ = attr.ib(
        metadata={"name": "and", "type": "element", "optional": True},
        type="CompositeFilterType",
        default=attr.NOTHING,
    )
    or_ = attr.ib(
        metadata={"name": "or", "type": "element", "optional": True},
        type="CompositeFilterType",
        default=attr.NOTHING,
    )
    cat = attr.ib(
        metadata={"name": "cat", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    class_ = attr.ib(
        metadata={"name": "class", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    test = attr.ib(
        metadata={"name": "test", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    id_ = attr.ib(
        metadata={"name": "id", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    method = attr.ib(
        metadata={"name": "method", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    namespace = attr.ib(
        metadata={"name": "namespace", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    prop = attr.ib(
        metadata={"name": "prop", "type": "element", "optional": True},
        type="None",
        default=attr.NOTHING,
    )
    name = attr.ib(
        metadata={"name": "name", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )


@attr.s
class CompositeFilterType(object):
    not_ = attr.ib(
        metadata={"name": "not", "type": "element", "optional": True},
        type="None",
        default=attr.NOTHING,
    )
    and_ = attr.ib(
        metadata={"name": "and", "type": "element", "optional": True},
        type="CompositeFilterType",
        default=attr.NOTHING,
    )
    or_ = attr.ib(
        metadata={"name": "or", "type": "element", "optional": True},
        type="CompositeFilterType",
        default=attr.NOTHING,
    )
    cat = attr.ib(
        metadata={"name": "cat", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    class_ = attr.ib(
        metadata={"name": "class", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    test = attr.ib(
        metadata={"name": "test", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    id_ = attr.ib(
        metadata={"name": "id", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    method = attr.ib(
        metadata={"name": "method", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    namespace = attr.ib(
        metadata={"name": "namespace", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    prop = attr.ib(
        metadata={"name": "prop", "type": "element", "optional": True},
        type="None",
        default=attr.NOTHING,
    )
    name = attr.ib(
        metadata={"name": "name", "type": "element", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )


@attr.s
class ValueMatchFilterType(object):
    name = attr.ib(
        metadata={"name": "name", "type": "content", "optional": True},
        type="ValueMatchFilterType",
        default=attr.NOTHING,
    )
    re = attr.ib(
        metadata={"name": "re", "type": "attrib", "optional": True},
        type=bool,
        default=attr.NOTHING,
    )


@attr.s
class TestCaseElementType(object):
    properties = attr.ib(
        metadata={"name": "properties", "type": "element", "optional": False},
        type="PropertyBagType",
    )
    environment = attr.ib(
        metadata={"name": "environment", "type": "element", "optional": False},
        type="EnvironmentType",
    )
    settings = attr.ib(
        metadata={"name": "settings", "type": "element", "optional": True},
        type="SettingsType",
        default=attr.NOTHING,
    )
    failure = attr.ib(
        metadata={"name": "failure", "type": "element", "optional": True},
        type="FailureType",
        default=attr.NOTHING,
    )
    reason = attr.ib(
        metadata={"name": "reason", "type": "element", "optional": True},
        type="ReasonType",
        default=attr.NOTHING,
    )
    output = attr.ib(
        metadata={"name": "output", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    assertions = attr.ib(
        metadata={"name": "assertions", "type": "element", "optional": True},
        type="AssertionsType",
        default=attr.NOTHING,
    )
    attachments = attr.ib(
        metadata={"name": "attachments", "type": "element", "optional": True},
        type="AttachmentsType",
        default=attr.NOTHING,
    )
    id_ = attr.ib(
        metadata={"name": "id", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    name = attr.ib(
        metadata={"name": "name", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    fullname = attr.ib(
        metadata={"name": "fullname", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    methodname = attr.ib(
        metadata={"name": "methodname", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    classname = attr.ib(
        metadata={"name": "classname", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    runstate = attr.ib(
        metadata={"name": "runstate", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestRunStateType),
    )
    seed = attr.ib(
        metadata={"name": "seed", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    result = attr.ib(
        metadata={"name": "result", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestStatusType),
    )
    label = attr.ib(
        metadata={"name": "label", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    site = attr.ib(
        metadata={"name": "site", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )
    start_time = attr.ib(
        metadata={"name": "start-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    end_time = attr.ib(
        metadata={"name": "end-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    duration = attr.ib(
        metadata={"name": "duration", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )
    asserts = attr.ib(
        metadata={"name": "asserts", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )


@attr.s
class TestSuiteElementType(object):
    properties = attr.ib(
        metadata={"name": "properties", "type": "element", "optional": False},
        type="PropertyBagType",
    )
    test_suite = attr.ib(
        metadata={"name": "test-suite", "type": "element", "optional": True},
        type="TestSuiteElementType",
        default=attr.NOTHING,
    )
    test_case = attr.ib(
        metadata={"name": "test-case", "type": "element", "optional": True},
        type="TestCaseElementType",
        default=attr.NOTHING,
    )
    environment = attr.ib(
        metadata={"name": "environment", "type": "element", "optional": False},
        type="EnvironmentType",
    )
    settings = attr.ib(
        metadata={"name": "settings", "type": "element", "optional": True},
        type="SettingsType",
        default=attr.NOTHING,
    )
    failure = attr.ib(
        metadata={"name": "failure", "type": "element", "optional": True},
        type="FailureType",
        default=attr.NOTHING,
    )
    reason = attr.ib(
        metadata={"name": "reason", "type": "element", "optional": True},
        type="ReasonType",
        default=attr.NOTHING,
    )
    output = attr.ib(
        metadata={"name": "output", "type": "element", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    assertions = attr.ib(
        metadata={"name": "assertions", "type": "element", "optional": True},
        type="AssertionsType",
        default=attr.NOTHING,
    )
    attachments = attr.ib(
        metadata={"name": "attachments", "type": "element", "optional": True},
        type="AttachmentsType",
        default=attr.NOTHING,
    )
    id_ = attr.ib(
        metadata={"name": "id", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    name = attr.ib(
        metadata={"name": "name", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    fullname = attr.ib(
        metadata={"name": "fullname", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    methodname = attr.ib(
        metadata={"name": "methodname", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    classname = attr.ib(
        metadata={"name": "classname", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    runstate = attr.ib(
        metadata={"name": "runstate", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestRunStateType),
    )
    type_ = attr.ib(
        metadata={"name": "type", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestSuiteTypeType),
    )
    testcasecount = attr.ib(
        metadata={"name": "testcasecount", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    result = attr.ib(
        metadata={"name": "result", "type": "attrib", "optional": False},
        validator=attr.validators.in_(TestStatusType),
    )
    label = attr.ib(
        metadata={"name": "label", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    site = attr.ib(
        metadata={"name": "site", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )
    start_time = attr.ib(
        metadata={"name": "start-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    end_time = attr.ib(
        metadata={"name": "end-time", "type": "attrib", "optional": True},
        type=str,
        default=attr.NOTHING,
    )
    duration = attr.ib(
        metadata={"name": "duration", "type": "attrib", "optional": True},
        default=attr.NOTHING,
    )
    asserts = attr.ib(
        metadata={"name": "asserts", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    total = attr.ib(
        metadata={"name": "total", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    passed = attr.ib(
        metadata={"name": "passed", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    failed = attr.ib(
        metadata={"name": "failed", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    warnings = attr.ib(
        metadata={"name": "warnings", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    inconclusive = attr.ib(
        metadata={"name": "inconclusive", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )
    skipped = attr.ib(
        metadata={"name": "skipped", "type": "attrib", "optional": False},
        validator=attr.validators.instance_of(int),
    )


@attr.s
class PropertyBagType(object):
    property = attr.ib(
        metadata={"name": "property", "type": "element", "optional": False},
        type="PropertyType",
    )


@attr.s
class PropertyType(object):
    name = attr.ib(
        metadata={"name": "name", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
    value = attr.ib(
        metadata={"name": "value", "type": "attrib", "optional": False},
        type=str,
        validator=attr.validators.instance_of(str),
    )
