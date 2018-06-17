class Foo(object):
    def __new__(cls):
        return object.__new__(Foo)

class Bar(object):
    def __init_subclass__(cls):
        pass

class Meta(type):
    def __new__(cls, name, bases, attrs):
        pass
    def test(cls):
        pass

def bar():
    '''
        >>> class Foo(FooParent):
        ...     def bar(self):
        ...         pass
    '''
    pass
