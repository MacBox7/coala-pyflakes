import os
from queue import Queue

from pyflakes_bears.NoFutureImportBear import NoFutureImportBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.results.Result import Result
from coalib.results.Diff import Diff

def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'no_future_test_files',
                        name)

def load_testfile(name):
    with open(get_testfile_path(name)) as fl:
        contents = fl.read()
    contents = contents.splitlines(True)
    return contents

class NoFutureImportTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('no_future')
        self.uut = NoFutureImportBear(self.section, Queue())
        self.filename = 'NoFutureImportBear'

    def test_general(self):

        self.check_validity(self.uut, load_testfile('valid.py'))
        self.check_invalidity(self.uut, load_testfile('invalid.py'))

    def test_multiline_imports(self):
        self.filename = 'multiline_imports.py'
        file_text = load_testfile(self.filename)

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
        self.filename = 'compound_imports.py'
        file_text = load_testfile(self.filename)

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
        self.filename = 'multiline_compound_imports.py'
        file_text = load_testfile(self.filename)

        diff = Diff(file_text)
        diff.delete_lines(1, 2)
        diff.add_line(1, 'x = 2\n')

        # print('@'*50)
        # print(Result.from_values('NoFutureImportBear',
        #                     'Future import(s) found',
        #                     file=self.filename,
        #                     line=1,
        #                     diffs={self.filename: diff}))
        # print(diff.unified_diff)
        # print('@'*50)
        self.check_results(
            self.uut,
            file_text,
            [Result.from_values('NoFutureImportBear',
                                'Future import(s) found',
                                file=self.filename,
                                line=1,
                                diffs={self.filename: diff})],
            filename=self.filename)
