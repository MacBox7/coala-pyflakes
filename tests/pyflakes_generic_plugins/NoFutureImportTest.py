import ast
import unittest

from pyflakes.checker import Checker

from pyflakes_generic_plugins.NoFutureImport import NoFutureImport


class NoFutureImportTest(unittest.TestCase):

    def setUp(self):
        self.filename = 'NoFutureImport'

    def check_validity(self, file):
        tree = ast.parse(''.join(file))
        results = NoFutureImport(tree, self.filename).run()
        self.assertFalse(len(list(results)))

    def check_invalidity(self, file):
        tree = ast.parse(''.join(file))
        results = NoFutureImport(tree, self.filename).run()
        self.assertTrue(len(list(results)))

    def test_external_initialization(self):
        """
        Assert if provision for external initialization is present.
        Ensures that flake8 can initialize plugin with pyflakes
        instance.
        """
        file = ['import sys']
        tree = ast.parse(''.join(file))
        checker = Checker(tree, self.filename)
        no_future_instance = NoFutureImport(tree, self.filename)
        no_future_instance.checker = checker

        self.assertTrue(no_future_instance.module_scope)
        self.assertFalse(len(list(no_future_instance.run())))

    def test_valid(self):
        self.check_validity(['import sys'])
        self.check_validity(['from os import path'])
        self.check_validity(['from ..custom import something'])

    def test_invalid(self):
        self.check_invalidity(['from __future__ import division'])
        self.check_invalidity(['from __future__ import print_function, \\\n',
                               '                       division\n'])
        self.check_invalidity(['from __future__ import division, '
                               'print_function'])
        self.check_invalidity(['from __future__ import division;'])
