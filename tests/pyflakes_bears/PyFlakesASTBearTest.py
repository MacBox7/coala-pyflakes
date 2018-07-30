from queue import Queue
import unittest

from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import execute_bear
from pyflakes.checker import ClassScope
from pyflakes.checker import DoctestScope
from pyflakes.checker import FunctionScope
from pyflakes.checker import GeneratorScope
from pyflakes.checker import Importation
from pyflakes.checker import ModuleScope
from pyflakes.messages import UnusedImport

from pyflakes_bears.PyFlakesASTBear import PyFlakesASTBear


class PyFlakesASTBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('pyflakes-ast')
        self.uut = PyFlakesASTBear(self.section, Queue())
        self.filename = 'PyFlakesASTBearTemp'

    def test_module_scope(self):
        file_text = ['def foo():\n',
                     '  pass\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].module_scope)
            self.assertIsInstance(result[0].module_scope, ModuleScope)

    def test_class_scopes(self):
        file_text = ['class Foo():\n',
                     '  pass\n',
                     'class Bar():\n',
                     '  pass\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].class_scopes)
            self.assertEqual(len(result[0].class_scopes), 2)
            for scope in result[0].class_scopes:
                self.assertIsInstance(scope, ClassScope)

    def test_function_scopes(self):
        file_text = ['def Foo():\n',
                     '  pass\n',
                     'def Bar():\n',
                     '  pass\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].function_scopes)
            self.assertEqual(len(result[0].function_scopes), 2)
            for scope in result[0].function_scopes:
                self.assertIsInstance(scope, FunctionScope)

    def test_generator_scopes(self):
        file_text = ['(1 for a, b in [(1, 2)])\n',
                     '(1 for a, b in [(1, 2, 3)])\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].generator_scopes)
            self.assertEqual(len(result[0].generator_scopes), 2)
            for scope in result[0].generator_scopes:
                self.assertIsInstance(scope, GeneratorScope)

    def test_doctest_scopes(self):
        file_text = ['def foo():\n',
                     '  \'\'\'\n',
                     '      >>> m\n',
                     '  \'\'\'\n',
                     'return 1\n',
                     'def bar():\n',
                     '  \'\'\'\n',
                     '      >>> function_in_doctest():\n',
                     '      ...    global m\n',
                     '      ...    m = 50\n',
                     '  \'\'\'\n',
                     'return 1\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].doctest_scopes)
            self.assertEqual(len(result[0].doctest_scopes), 2)
            for scope in result[0].doctest_scopes:
                self.assertIsInstance(scope, DoctestScope)

    def test_pyflakes_messages(self):
        file_text = ['import sys\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            self.assertIsNotNone(result[0].pyflakes_messages)
            self.assertEqual(len(result[0].pyflakes_messages), 1)
            self.assertIsInstance(result[0].pyflakes_messages[0], UnusedImport)

    def test_get_nodes(self):
        file_text = ['import sys\n',
                     'import os\n']

        with execute_bear(self.uut, self.filename, file_text) as result:
            module_scope = result[0].module_scope
            import_nodes = list(result[0].get_nodes(module_scope, Importation))
            self.assertEqual(len(import_nodes), 2)
            for node in import_nodes:
                self.assertIsInstance(node, Importation)
