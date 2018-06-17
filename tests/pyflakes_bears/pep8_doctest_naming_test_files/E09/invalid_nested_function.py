class Foo:
    def good(self):
        class Bar:
            def foo_bar():
                pass

def foo():
    '''
        >>> class Good():
        ...     def __str__(self):
        ...         class Bar:
        ...             def foo_bar(me):
        ...                 pass
    '''
    pass
