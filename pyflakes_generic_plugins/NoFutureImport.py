from pyflakes.checker import Checker
from pyflakes.checker import FutureImportation
from pyflakes.checker import ModuleScope

__version__ = '0.1'

CODE = 'F482'


class NoFutureImport(object):
    """
    NoFutureImport plugin implementation.

    A generic plugin that uses pyflakes AST to detect use of `__future__`
    import in python code.
    """

    name = 'no_future'
    version = __version__

    def __init__(self, tree, filename):
        """
        Allow flake8 to initialize plugin.

        :param tree:       The python AST tree object
        :param filename:   The filename of the file
        """
        self.tree = tree
        self.filename = filename
        self._checker = None
        self._module_scope = None

    @property
    def checker(self):
        """
        Property implemented for checker.

        Return the checker instance. If an instance is
        already provided use that.
        """
        if self._checker is None:
            self._checker = Checker(self.tree, self.filename)
        return self._checker

    @checker.setter
    def checker(self, checker):
        self._checker = checker

    @property
    def module_scope(self):
        """
        Property implemented for module_scope.

        Return the module_scope instance.
        """
        if self._module_scope is None:
            self._module_scope = list(filter(lambda scope:
                                             isinstance(scope,
                                                        ModuleScope),
                                             self.checker.deadScopes))[0]
        return self._module_scope

    def run(self):
        """
        Yield __future__ nodes.

        Traverses all nodes in the module scope and searches
        for FutureImportation nodes.
        """
        for _, node in self.module_scope.items():
            if isinstance(node, FutureImportation):
                message = ('{code}: Future import {name} found'
                           .format(name=node.name,
                                   code=CODE))
                yield (node.source.lineno, node.source.col_offset,
                       message, NoFutureImport)
