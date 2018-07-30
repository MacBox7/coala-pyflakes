import os
from queue import Queue

from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from pyflakes_bears.PEP8NamingBear import PEP8NamingBear


def get_testfile_path(directory, name):
    return os.path.join(os.path.dirname(__file__),
                        'pep8_naming_test_files',
                        directory,
                        name)


def load_testfile(directory, name):
    with open(get_testfile_path(directory, name)) as fl:
        contents = fl.read()
    contents = contents.splitlines(True)
    return contents


class PEP8NamingBearTest(LocalBearTestHelper):

    def setUp(self):
        self.madDiff = None
        self.section = Section('PEP8NamingBear')
        self.uut = PEP8NamingBear(self.section, Queue(),
                                  debugger=None, timeout=None)
        self.error_codes = PEP8NamingBear.ErrorCodes

    def test_e01(self):
        self.section.append(Setting('ignore',
                                    'ignored'))

        self.check_validity(self.uut, load_testfile('E01', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E01', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E01.format(name='GOOD',
                                                            asname='bad'),
                                file='invalid.py',
                                line=3,
                                end_line=3)],
            filename='invalid.py')

    def test_e02(self):
        self.check_validity(self.uut, load_testfile('E02', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E02', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E02.format(name='good',
                                                            asname='Bad'),
                                file='invalid.py',
                                line=3,
                                end_line=3)],
            filename='invalid.py')

    def test_e03(self):
        self.check_validity(self.uut, load_testfile('E03', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E03', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E03.format(name='GoodFile',
                                                            asname='bad'),
                                file='invalid.py',
                                line=3,
                                end_line=3)],
            filename='invalid.py')

    def test_e04(self):
        self.check_validity(self.uut, load_testfile('E04', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E04', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E04.format(name='CamelCase',
                                                            asname='CONST'),
                                file='invalid.py',
                                line=3,
                                end_line=3)],
            filename='invalid.py')

    def test_e05(self):
        self.section.append(Setting('ignore',
                                    'ignored'))

        self.check_validity(self.uut, load_testfile('E05', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E05', 'invalid_class.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E05.format(name='bad'),
                                file='invalid_class.py',
                                line=3,
                                end_line=3)],
            filename='invalid_class.py')

        self.check_results(
            self.uut,
            load_testfile('E05', 'invalid_underscore_name.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E05.format(name='_'),
                                file='invalid_underscore_name.py',
                                line=3,
                                end_line=3)],
            filename='invalid_underscore_name.py')

        self.check_results(
            self.uut,
            load_testfile('E05', 'invalid_nested_class.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E05.format(name='bad'),
                                file='invalid_nested_class.py',
                                line=4,
                                end_line=4)],
            filename='invalid_nested_class.py')

    def test_e06(self):
        self.check_validity(self.uut, load_testfile('E06', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E06', 'invalid_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E06.format(name='NotOk'),
                                file='invalid_function.py',
                                line=3,
                                end_line=3)],
            filename='invalid_function.py')

        self.check_results(
            self.uut,
            load_testfile('E06', 'invalid_nested_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E06.format(name='NotOk'),
                                file='invalid_nested_function.py',
                                line=4,
                                end_line=4)],
            filename='invalid_nested_function.py')

    def test_e07(self):
        self.check_validity(self.uut, load_testfile('E07', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E07', 'invalid_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E07,
                                file='invalid_function.py',
                                line=1,
                                end_line=1),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E07,
                                file='invalid_function.py',
                                line=6,
                                end_line=6)],
            filename='invalid_function.py')

        self.check_results(
            self.uut,
            load_testfile('E07', 'invalid_nested_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E07,
                                file='invalid_nested_function.py',
                                line=5,
                                end_line=5)],
            filename='invalid_nested_function.py')

    def test_e08(self):
        self.check_validity(self.uut, load_testfile('E08', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E08', 'invalid_function_args.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E08.format(name='BAD'),
                                file='invalid_function_args.py',
                                line=1,
                                column=9),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E08.format(name='VERYBAD'),
                                file='invalid_function_args.py',
                                line=3,
                                column=21)],
            filename='invalid_function_args.py')

        self.check_results(
            self.uut,
            load_testfile('E08', 'invalid_nested_function_args.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E08.format(name='BAD'),
                                file='invalid_nested_function_args.py',
                                line=5,
                                column=30),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E08.format(name='VERYBAD'),
                                file='invalid_nested_function_args.py',
                                line=12,
                                column=17)],
            filename='invalid_nested_function_args.py')

    def test_e09(self):
        self.section.append(Setting('ignore',
                                    'ignored'))

        self.check_validity(self.uut, load_testfile('E09', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E09', 'invalid_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E09,
                                file='invalid_function.py',
                                line=2,
                                end_line=2),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E09,
                                file='invalid_function.py',
                                line=8,
                                end_line=8)],
            filename='invalid_function.py')

        self.check_results(
            self.uut,
            load_testfile('E09', 'invalid_nested_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E09,
                                file='invalid_nested_function.py',
                                line=4,
                                end_line=4),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E09,
                                file='invalid_nested_function.py',
                                line=12,
                                end_line=12)],
            filename='invalid_nested_function.py')

    def test_e10(self):
        self.section.append(Setting('class_method_decorators',
                                    'classproperty'))

        self.check_validity(self.uut, load_testfile('E10', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E10', 'invalid_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E10,
                                file='invalid_function.py',
                                line=2,
                                end_line=2),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E10,
                                file='invalid_function.py',
                                line=9,
                                end_line=9)],
            filename='invalid_function.py')

        self.check_results(
            self.uut,
            load_testfile('E10', 'invalid_nested_function.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E10,
                                file='invalid_nested_function.py',
                                line=4,
                                end_line=4),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E10,
                                file='invalid_nested_function.py',
                                line=13,
                                end_line=13)],
            filename='invalid_nested_function.py')

    def test_e11(self):
        self.check_validity(self.uut, load_testfile('E11', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E11', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E11.format(name='mix_Case'),
                                file='invalid.py',
                                line=2,
                                column=6),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E11.format(name='mix_Case'),
                                file='invalid.py',
                                line=7,
                                column=17)],
            filename='invalid.py')

    def test_e12(self):
        self.check_validity(self.uut, load_testfile('E12', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E12', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E12.format(name='__mC'),
                                file='invalid.py',
                                line=1,
                                column=1),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E12.format(name='__mC'),
                                file='invalid.py',
                                line=5,
                                column=13)],
            filename='invalid.py')

    def test_e13(self):
        self.check_validity(self.uut, load_testfile('E13', 'valid.py'))

        self.check_results(
            self.uut,
            load_testfile('E13', 'invalid.py'),
            [Result.from_values('PEP8NamingBear',
                                self.error_codes.E13.format(name='Var1'),
                                file='invalid.py',
                                line=2,
                                column=5),
             Result.from_values('PEP8NamingBear',
                                self.error_codes.E13.format(name='Var1'),
                                file='invalid.py',
                                line=7,
                                column=17)],
            filename='invalid.py')
