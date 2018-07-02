import ast

from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result
from pyflakes.checker import Checker
from pyflakes.checker import ClassDefinition, FunctionDefinition
from pyflakes.checker import (ModuleScope, ClassScope, FunctionScope,
                              GeneratorScope, DoctestScope)


class PyFlakesChecker(Checker):
    def __init__(self, tree, filename='(none)', builtins=None,
                 withDoctest=False):
        super().__init__(tree, filename='(none)', builtins=None,
                         withDoctest=False)

    def ARGUMENTS(self, node):
        pass


class PyFlakesResult(HiddenResult):

    def __init__(self, origin, deadScopes, pyflakes_messages):

        Result.__init__(self, origin, message='')

        self.module_scope = self.get_scopes(ModuleScope, deadScopes)[0]
        self.class_scopes = self.get_scopes(ClassScope, deadScopes)
        self.function_scopes = self.get_scopes(FunctionScope, deadScopes)
        self.generator_scopes = self.get_scopes(GeneratorScope, deadScopes)
        self.doctest_scopes = self.get_scopes(DoctestScope, deadScopes)
        self.pyflakes_messages = pyflakes_messages

    def get_scopes(self, scope_type, scopes):
        return list(filter(lambda scope: type(scope) == scope_type,
                           scopes))

    def get_nodes(self, scope, node_type):
        for _, node in scope.items():
            if type(node) == node_type:
                yield node

    def get_node_scope(self, node):
        result = PyFlakesChecker(node.source, filename='')
        scope = self.get_scopes(ModuleScope, result.deadScopes)[0]
        scope.parent = node
        return scope

    def get_class_definitions(self, module_scope, parent=None):
        result = list()
        for _, node in module_scope.items():
            node.parent = parent
            if type(node) == ClassDefinition:
                result.append(node)
            if any([type(node) == ClassDefinition,
                    type(node) == FunctionDefinition]):
                result.extend(self.get_class_definitions(
                    self.get_node_scope(node), node))
        return result

    def get_function_definitions(self, module_scope, parent=None):
        result = list()
        for _, node in module_scope.items():
            node.parent = parent
            if type(node) == FunctionDefinition:
                result.append(node)
            if any([type(node) == ClassDefinition,
                    type(node) == FunctionDefinition]):
                result.extend(self.get_function_definitions(
                    self.get_node_scope(node), node))
        return result


class PyFlakesASTBear(LocalBear):
    """
    PyFlakesASTBear is a meta bear that generates pyflakes-enhance-AST
    for the input file and provides the results as a HiddenResult object
    to the bear that depends on it.

    Examples of bears that can be constructed using PyFlakesASTBear are:

    -   A NoFutureImportBear that checks a file for use of any `__future__`
        import statement
    -   A PEP8DoctestNamingBear that checks if the python code written in
        docstring follows PEP8 naming convention
    """

    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file):
        tree = ast.parse(''.join(file))
        result = Checker(tree, filename=filename, withDoctest=True)

        yield PyFlakesResult(self, result.deadScopes, result.messages)
