import attr

@attr.s
class TestDurationType(float):
    pass


@attr.s
class NonnegativeInt32(int):
    pass


@attr.s
class TestRunType(object):
    id = attr.ib(metadata={"name": 'id'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname'}, type=str, validator=attr.validators.instance_of(str))
    testcasecount = attr.ib(metadata={"name": 'testcasecount'}, validator=attr.validators.instance_of(NonnegativeInt32))
    result = attr.ib(metadata={"name": 'result'}, validator=attr.validators.instance_of(None))
    label = attr.ib(metadata={"name": 'label'}, type=str, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration'}, default=attr.NOTHING)
    total = attr.ib(metadata={"name": 'total'}, validator=attr.validators.instance_of(NonnegativeInt32))
    passed = attr.ib(metadata={"name": 'passed'}, validator=attr.validators.instance_of(NonnegativeInt32))
    failed = attr.ib(metadata={"name": 'failed'}, validator=attr.validators.instance_of(NonnegativeInt32))
    inconclusive = attr.ib(metadata={"name": 'inconclusive'}, validator=attr.validators.instance_of(NonnegativeInt32))
    skipped = attr.ib(metadata={"name": 'skipped'}, validator=attr.validators.instance_of(NonnegativeInt32))
    asserts = attr.ib(metadata={"name": 'asserts'}, validator=attr.validators.instance_of(NonnegativeInt32))
    random_seed = attr.ib(metadata={"name": 'random-seed'}, type=int, validator=attr.validators.instance_of(int))


@attr.s
class TestFilterType(object):
    pass


@attr.s
class CompositeFilterType(object):
    pass


@attr.s
class ValueMatchFilterType(object):
    re = attr.ib(metadata={"name": 're'}, type=bool, default=attr.NOTHING)


@attr.s
class TestCaseElementType(object):
    id = attr.ib(metadata={"name": 'id'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname'}, type=str, validator=attr.validators.instance_of(str))
    methodname = attr.ib(metadata={"name": 'methodname'}, type=str, default=attr.NOTHING)
    classname = attr.ib(metadata={"name": 'classname'}, type=str, default=attr.NOTHING)
    runstate = attr.ib(metadata={"name": 'runstate'}, validator=attr.validators.instance_of(None))
    seed = attr.ib(metadata={"name": 'seed'}, type=str, validator=attr.validators.instance_of(str))
    result = attr.ib(metadata={"name": 'result'}, validator=attr.validators.instance_of(None))
    label = attr.ib(metadata={"name": 'label'}, type=str, default=attr.NOTHING)
    site = attr.ib(metadata={"name": 'site'}, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration'}, default=attr.NOTHING)
    asserts = attr.ib(metadata={"name": 'asserts'}, validator=attr.validators.instance_of(NonnegativeInt32))


@attr.s
class TestSuiteElementType(object):
    id = attr.ib(metadata={"name": 'id'}, type=str, validator=attr.validators.instance_of(str))
    name = attr.ib(metadata={"name": 'name'}, type=str, validator=attr.validators.instance_of(str))
    fullname = attr.ib(metadata={"name": 'fullname'}, type=str, validator=attr.validators.instance_of(str))
    methodname = attr.ib(metadata={"name": 'methodname'}, type=str, default=attr.NOTHING)
    classname = attr.ib(metadata={"name": 'classname'}, type=str, default=attr.NOTHING)
    runstate = attr.ib(metadata={"name": 'runstate'}, validator=attr.validators.instance_of(None))
    type = attr.ib(metadata={"name": 'type'}, validator=attr.validators.instance_of(None))
    testcasecount = attr.ib(metadata={"name": 'testcasecount'}, validator=attr.validators.instance_of(NonnegativeInt32))
    result = attr.ib(metadata={"name": 'result'}, validator=attr.validators.instance_of(None))
    label = attr.ib(metadata={"name": 'label'}, type=str, default=attr.NOTHING)
    site = attr.ib(metadata={"name": 'site'}, default=attr.NOTHING)
    start_time = attr.ib(metadata={"name": 'start-time'}, type=str, default=attr.NOTHING)
    end_time = attr.ib(metadata={"name": 'end-time'}, type=str, default=attr.NOTHING)
    duration = attr.ib(metadata={"name": 'duration'}, default=attr.NOTHING)
    asserts = attr.ib(metadata={"name": 'asserts'}, validator=attr.validators.instance_of(NonnegativeInt32))
    total = attr.ib(metadata={"name": 'total'}, validator=attr.validators.instance_of(NonnegativeInt32))
    passed = attr.ib(metadata={"name": 'passed'}, validator=attr.validators.instance_of(NonnegativeInt32))
    failed = attr.ib(metadata={"name": 'failed'}, validator=attr.validators.instance_of(NonnegativeInt32))
    warnings = attr.ib(metadata={"name": 'warnings'}, validator=attr.validators.instance_of(NonnegativeInt32))
    inconclusive = attr.ib(metadata={"name": 'inconclusive'}, validator=attr.validators.instance_of(NonnegativeInt32))
    skipped = attr.ib(metadata={"name": 'skipped'}, validator=attr.validators.instance_of(NonnegativeInt32))


