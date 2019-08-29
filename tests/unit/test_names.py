from pytest_nunit.nunit import get_node_names


def test_names():
    """
    Test basic split of module::test
    """
    a = "x::y"
    b = get_node_names(a)
    assert b == ('x', 'y')


def  test_name():
    """
    Test split of module::class::test
    """
    x = "x::y::z"
    y= get_node_names(x)
    assert y == ('y', 'z')


def test_words():
    """
    Test split of module::class::test
    """
    a ="boo::foo::doo" 
    b = get_node_names(a) 
    assert b == ('foo', 'doo')
