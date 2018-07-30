def __getattr__():
    pass

class C1:
    def __str__(self):
        return ''

    def foo(self):
        '''
            >>> class Good():
            ...     def __str__(self):
            ...         return 1
        '''
        pass

class C2:
    if True:
        def __str__(self):
            return ''

class C3:
    try:
        if True:
            while True:
                def __str__(self):
                    return ''
                break
    except:
        pass
