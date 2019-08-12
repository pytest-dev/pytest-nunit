from pytest_nunit.nunit import get_node_names
class TestInt:

    def test_names(self):
        a = "x::y"
        b = get_node_names(a)
        assert b == ('x', 'y')


    def  test_name(self):
        x = "x::y::z"
        y= get_node_names(x)
        assert y == ( 'y', 'z')
       
    def test_words(self):
        a ="boo::foo::doo" 
        b = get_node_names(a) 
        assert b == ('foo', 'doo')