import attr

@attr.s
class TestDurationType(object):


@attr.s
class NonnegativeInt32(object):


@attr.s
class TestRunType(object):
    id = attr.ib(type=object)
    name = attr.ib(type=object)
    fullname = attr.ib(type=object)
    testcasecount = attr.ib()
    result = attr.ib()
    label = attr.ib(type=object)
    start-time = attr.ib(type=object)
    end-time = attr.ib(type=object)
    duration = attr.ib()
    total = attr.ib()
    passed = attr.ib()
    failed = attr.ib()
    inconclusive = attr.ib()
    skipped = attr.ib()
    asserts = attr.ib()
    random-seed = attr.ib(type=object)


@attr.s
class TestFilterType(object):


@attr.s
class CompositeFilterType(object):


@attr.s
class ValueMatchFilterType(object):
    re = attr.ib(type=object)


@attr.s
class TestCaseElementType(object):
    id = attr.ib(type=object)
    name = attr.ib(type=object)
    fullname = attr.ib(type=object)
    methodname = attr.ib(type=object)
    classname = attr.ib(type=object)
    runstate = attr.ib()
    seed = attr.ib(type=object)
    result = attr.ib()
    label = attr.ib(type=object)
    site = attr.ib()
    start-time = attr.ib(type=object)
    end-time = attr.ib(type=object)
    duration = attr.ib()
    asserts = attr.ib()


@attr.s
class TestSuiteElementType(object):
    id = attr.ib(type=object)
    name = attr.ib(type=object)
    fullname = attr.ib(type=object)
    methodname = attr.ib(type=object)
    classname = attr.ib(type=object)
    runstate = attr.ib()
    type = attr.ib()
    testcasecount = attr.ib()
    result = attr.ib()
    label = attr.ib(type=object)
    site = attr.ib()
    start-time = attr.ib(type=object)
    end-time = attr.ib(type=object)
    duration = attr.ib()
    asserts = attr.ib()
    total = attr.ib()
    passed = attr.ib()
    failed = attr.ib()
    warnings = attr.ib()
    inconclusive = attr.ib()
    skipped = attr.ib()


