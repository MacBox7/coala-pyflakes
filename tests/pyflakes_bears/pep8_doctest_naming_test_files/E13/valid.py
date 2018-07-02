def foo():
    good = 1

def bar():
    def foo_bar():
        good = 1

GOOD = 1

class Foo(object):
    GOOD = 1

def fun():
    with FOO() as foo, bar() as bar:
        pass

def ok():
    with suppress(E):
        pass
    with contextlib.suppress(E):
        pass

with Test() as bar:
    pass

def test():
    with C() as [a, b, c]:
        pass
