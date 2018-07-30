import ast

from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result
from pyflakes.checker import Argument
from pyflakes.checker import Checker
from pyflakes.checker import ClassDefinition
from pyflakes.checker import ClassScope
from pyflakes.checker import DoctestScope
from pyflakes.checker import FunctionDefinition
from pyflakes.checker import FunctionScope
from pyflakes.checker import GeneratorScope
from pyflakes.checker import ModuleScope


class PyFlakesChecker(Checker):
    """
    Subclass of Checker class.

    Fixes node information of arguments and creates link
    between scope and their corresponding nodes.
    """

    def handleNode(self, node, parent):
        """
        Link scope with their corresponding nodes.

        :param node:       The ast node being handled.
        :param parent:     Parent node.
        """
        if (isinstance(self.scope, (ClassScope, FunctionScope)) and
                not hasattr(self.scope, '_node')):
            self.scope._node = parent
        parent._scope = self.scope
        super().handleNode(node, parent)

    def ARG(self, node):
        """
        Fix location information of arguments.

        :param node:       The ast node being handled.
        """
        self.addBinding(node, Argument(node.arg, node))


class PyFlakesResult(HiddenResult):
    """
    Formats output of the metabear.

    Provides module_scope, class_scopes, function_scopes, generator_scopes,
    doctest_scopes and pyflakes_messages to the dependent bear. Also
    provides them with get_scopes, get_nodes and get_all_nodes
    helper functions.
    """

    def __init__(self, origin, deadScopes, pyflakes_messages):
        """
        Initialize the results object.

        :param origin:            The origin of invocation
        :param deadScopes:        Deadscopes returned by pyflakes
        :param pyflakes_messages: A list of warnings detected by pyflakes
        """
        Result.__init__(self, origin, message='')

        self.module_scope = self.get_scopes(ModuleScope, deadScopes)[0]
        self.class_scopes = self.get_scopes(ClassScope, deadScopes)
        self.function_scopes = self.get_scopes(FunctionScope, deadScopes)
        self.generator_scopes = self.get_scopes(GeneratorScope, deadScopes)
        self.doctest_scopes = self.get_scopes(DoctestScope, deadScopes)
        self.pyflakes_messages = pyflakes_messages

    def sort_nodes(fn):
        """
        Decorate functions to return list of sorted nodes.

        `key` and `reverse` are the additional parameter that can be
        passed to a function. These parameters will be used to sort
        the nodes.

        :param fn:   The function to be decorated.
        :return:     Decorated function that returns sorted list.
        """
        def wrap(*args, **kwargs):
            result = list(fn(*args, **kwargs))
            if 'key' in kwargs:
                result = sorted(result,
                                key=kwargs.get('key'),
                                reverse=kwargs.get('reverse', False))
            return result

        return wrap

    def get_scopes(self, scope_type, scopes):
        """
        Get scopes of a specific type.

        :param scope_type:   The type of scope to be filtered.
        :param scopes:       The list of scopes.
        :return:             A list of filtered scopes.
        """
        return list(filter(lambda scope: type(scope) == scope_type,
                           scopes))

    @sort_nodes
    def get_nodes(self, scope, node_type, **kwargs):
        """
        Yield nodes of a specific type.

        :param scope:      The scope to be searched in.
        :param node_type:  The type of node to be filtered.
        :param **kwargs:
            - `key`:       The key using which nodes should be sorted.
            - `reverse`:   bool flag to reverse sort order.
        """
        for _, node in scope.items():
            if type(node) == node_type:
                yield node

    @sort_nodes
    def get_all_nodes(self, scope, node_type, parent=None, **kwargs):
        """
        Recusively look for nodes inside a scope.

        :param scope:       The type of scope to be filtered.
        :param node_type:   The list of scopes.
        :param parent:      The parent of node.
        :param **kwargs:
            - `key`:       The key using which nodes should be sorted.
            - `reverse`:   bool flag to reverse sort order.
        """
        for _, node in scope.items():
            node.parent = parent
            if type(node) == node_type:
                yield node
            if (hasattr(node.source, '_scope') and
                    isinstance(node, (ClassDefinition, FunctionDefinition))):
                yield from self.get_all_nodes(node.source._scope,
                                              node_type, node, **kwargs)


class PyFlakesASTBear(LocalBear):
    """
    A meta bear to wrap pyflakes-enhance-AST.

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
        """
        Yield HiddenResult node containing pyflakes ast.

        :param filename:   The name of the file
        :param file:       The content of the file
        """
        tree = ast.parse(''.join(file))
        result = PyFlakesChecker(tree, filename=filename, withDoctest=True)

        yield PyFlakesResult(self, result.deadScopes, result.messages)
