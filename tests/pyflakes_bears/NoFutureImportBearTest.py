from queue import Queue

from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from pyflakes_bears.NoFutureImportBear import NoFutureImportBear


class NoFutureImportTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('no_future')
        self.uut = NoFutureImportBear(self.section, Queue())
        self.filename = 'NoFutureImportBear'

    def test_valid(self):
        self.check_validity(self.uut, ['import sys'])
        self.check_validity(self.uut, ['from os import path'])
        self.check_validity(self.uut, ['from ..custom import something'])

    def test_invalid(self):
        self.check_invalidity(self.uut, ['from __future__ import division'])
        self.check_invalidity(self.uut,
                              ['from __future__ import print_function, \\\n',
                               '                       division\n'])
        self.check_invalidity(self.uut,
                              ['from __future__ import division, '
                               'print_function'])
        self.check_invalidity(self.uut, ['from __future__ import division;'])

    def test_multiline_imports(self):
        file_text = ['from __future__ import with_statement, \\\n',
                     '                       print_function, \\\n',
                     '                       generators\n']

        diff = Diff(file_text)
        diff.delete_lines(1, 3)

        self.check_results(
            self.uut,
            file_text,
            [Result.from_values('NoFutureImportBear',
                                'Future import(s) found',
                                file=self.filename,
                                line=1,
                                diffs={self.filename: diff},
                                end_line=1)],
            filename=self.filename)

    def test_compound_imports(self):
        file_text = ['from __future__ import unicode_literals;'
                     'from __future__ import nested_scopes; x = 2;\n']

        diff = Diff(file_text)
        diff.modify_line(1, 'x = 2;\n')

        self.check_results(
            self.uut,
            file_text,
            [Result.from_values('NoFutureImportBear',
                                'Future import(s) found',
                                file=self.filename,
                                line=1,
                                diffs={self.filename: diff},
                                end_line=1)],
            filename=self.filename)

    def test_multiline_compound_imports(self):
        file_text = ['from __future__ import nested_scopes, \\\n',
                     '                       generators;'
                     'from __future__ import absolute_import;'
                     'x = 2\n']

        diff = Diff(file_text)
        diff.delete_lines(1, 2)
        diff.add_line(1, 'x = 2\n')

        self.check_results(
            self.uut,
            file_text,
            [Result.from_values('NoFutureImportBear',
                                'Future import(s) found',
                                file=self.filename,
                                line=1,
                                diffs={self.filename: diff},
                                end_line=1)],
            filename=self.filename)
