class Foo(type):
    def __new__(cls, name):
        pass

    @classmethod
    def test(cls):
        pass

def bar():
    '''
        >>> class Foo(FooParent):
        ...     @classproperty
        ...     def bar(cls):
        ...         pass
    '''
    pass
