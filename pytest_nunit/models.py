import attr
import enum


@attr.s
class TestFilterType(object):
    pass


class TestDurationType(float):
    pass


class TestResultType(enum.Enum):
    Inconclusive = 'Inconclusive'
    Skipped = 'Skipped'
    Passed = 'Passed'
    Warning = 'Warning'
    Failed = 'Failed'


class NonnegativeInt32(int):
    pass


@attr.s
class TestRunType(object):
    command_line = attr.ib(metadata={"name": 'command-line', "type": 'element'}, type=str)
    filter = attr.ib(metadata={"name": 'filter', "type": 'element'}, type=TestFilterType, validator=attr.validators.instance_of(TestFilterType))
    id_ = attr.ib(metadata={"name": 'id', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    testcasecount = attr.ib(metadata={"name": 'testcasecount', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    result = attr.ib(metadata={"name": 'result', "type": 'attrib'}, validator=attr.validators.in_(TestResultType))
    label = attr.ib(metadata={"name": 'label', "type": 'attrib'}, type=str, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration', "type": 'attrib'}, default=attr.NOTHING)
    total = attr.ib(metadata={"name": 'total', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    passed = attr.ib(metadata={"name": 'passed', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    failed = attr.ib(metadata={"name": 'failed', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    inconclusive = attr.ib(metadata={"name": 'inconclusive', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    skipped = attr.ib(metadata={"name": 'skipped', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    asserts = attr.ib(metadata={"name": 'asserts', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    random_seed = attr.ib(metadata={"name": 'random-seed', "type": 'attrib'}, type=int, validator=attr.validators.instance_of(int))


@attr.s
class CompositeFilterType(object):
    pass


@attr.s
class ValueMatchFilterType(object):
    re = attr.ib(metadata={"name": 're', "type": 'attrib'}, type=bool, default=attr.NOTHING)


@attr.s
class TestCaseElementType(object):
    id_ = attr.ib(metadata={"name": 'id', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    methodname = attr.ib(metadata={"name": 'methodname', "type": 'attrib'}, type=str, default=attr.NOTHING)
    classname = attr.ib(metadata={"name": 'classname', "type": 'attrib'}, type=str, default=attr.NOTHING)
    runstate = attr.ib(metadata={"name": 'runstate', "type": 'attrib'}, validator=attr.validators.in_(None))
    seed = attr.ib(metadata={"name": 'seed', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    result = attr.ib(metadata={"name": 'result', "type": 'attrib'}, validator=attr.validators.in_(None))
    label = attr.ib(metadata={"name": 'label', "type": 'attrib'}, type=str, default=attr.NOTHING)
    site = attr.ib(metadata={"name": 'site', "type": 'attrib'}, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration', "type": 'attrib'}, default=attr.NOTHING)
    asserts = attr.ib(metadata={"name": 'asserts', "type": 'attrib'}, validator=attr.validators.instance_of(int))


@attr.s
class TestSuiteElementType(object):
    id_ = attr.ib(metadata={"name": 'id', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname', "type": 'attrib'}, type=str, validator=attr.validators.instance_of(str))
    methodname = attr.ib(metadata={"name": 'methodname', "type": 'attrib'}, type=str, default=attr.NOTHING)
    classname = attr.ib(metadata={"name": 'classname', "type": 'attrib'}, type=str, default=attr.NOTHING)
    runstate = attr.ib(metadata={"name": 'runstate', "type": 'attrib'}, validator=attr.validators.in_(None))
    type_ = attr.ib(metadata={"name": 'type', "type": 'attrib'}, validator=attr.validators.in_(None))
    testcasecount = attr.ib(metadata={"name": 'testcasecount', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    result = attr.ib(metadata={"name": 'result', "type": 'attrib'}, validator=attr.validators.in_(None))
    label = attr.ib(metadata={"name": 'label', "type": 'attrib'}, type=str, default=attr.NOTHING)
    site = attr.ib(metadata={"name": 'site', "type": 'attrib'}, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time', "type": 'attrib'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration', "type": 'attrib'}, default=attr.NOTHING)
    asserts = attr.ib(metadata={"name": 'asserts', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    total = attr.ib(metadata={"name": 'total', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    passed = attr.ib(metadata={"name": 'passed', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    failed = attr.ib(metadata={"name": 'failed', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    warnings = attr.ib(metadata={"name": 'warnings', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    inconclusive = attr.ib(metadata={"name": 'inconclusive', "type": 'attrib'}, validator=attr.validators.instance_of(int))
    skipped = attr.ib(metadata={"name": 'skipped', "type": 'attrib'}, validator=attr.validators.instance_of(int))


