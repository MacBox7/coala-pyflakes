from collections import namedtuple

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from pyflakes_bears.PyFlakesASTBear import PyFlakesASTBear
from pyflakes.checker import (ClassDefinition, Importation,
                              ImportationFrom, Binding,
                              FunctionDefinition, Assignment,
                              Argument)


class PEP8DoctestNamingBear(LocalBear):
    """
    Uses pyflakes-enhance-AST to remove future imports
    """

    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    BEAR_DEPS = {PyFlakesASTBear}

    class ErrorCodes:
        E01 = 'constant {name} imported as non constant {asname}'
        E02 = 'lowercase {name} imported as non lowercase {asname}'
        E03 = 'camelcase {name} imported as lowercase {asname}'
        E04 = 'camelcase {name} imported as constant {asname}'
        E05 = 'class name {name} should use CapWords convention'
        E06 = 'function name {name} should be lowercase'
        E07 = 'function name should not start or end with __'
        E08 = 'argument name {name} should be lowercase'
        E09 = 'first argument of a method should be named self'
        E10 = 'first argument of a classmethod should be named cls'
        E11 = 'variable {name} in class scope should not be mixedCase'
        E12 = 'variable {name} in module scope should not be mixedCase'
        E13 = 'variable {name} in function should be lowercase'

    def is_valid_class_name(self, node):
        name = node.name
        return name.lstrip('_')[:1].isupper()

    def is_valid_function_name(self, node):
        ignore_names = ['setUp', 'tearDown', 'setUpClass', 'tearDownClass']
        name = node.name
        if name in ignore_names:
            return True
        return name.islower() and name != '_'

    def check_method_arg(self, node):
        if not type(node.parent) == ClassDefinition:
            return True
        # If this class inherits from `type`, it's a metaclass, and we'll
        # consider all of it's methods to be classmethods.
        cls_bases = node.parent.source.bases
        if any(name for name in cls_bases
               if hasattr(name, 'id') and name.id == 'type'):
            return True
        # Check if they are not classmethod or staticmethod
        exceptions = ['classmethod', 'staticmethod', 'classproperty']
        decorator_list = (node.id for node in node.source.decorator_list
                          if hasattr(node, 'id'))
        if any(map(lambda each: each in exceptions, decorator_list)):
            return True
        # Reserved names for classmethod
        if node.name in ('__new__', '__init_subclass__'):
            return True
        # Check for the name of the first argument
        if not node.source.args or not len(node.source.args.args):
            return False
        first_arg = node.source.args.args[0]
        if first_arg.arg != 'self':
            return False
        return True

    def check_class_method_arg(self, node):
        if not type(node.parent) == ClassDefinition:
            return True
        # Check if it is a classmethod
        decorator_list = (node.id for node in node.source.decorator_list
                          if hasattr(node, 'id'))
        # List of decorators used for declaring class methods
        whitelisted = ['classmethod', 'classproperty']
        if not any(map(lambda each: each in whitelisted, decorator_list)):
            # If this class inherits from `type`, it's a metaclass, and we'll
            # consider all of it's methods to be classmethods.
            cls_bases = node.parent.source.bases
            if not any(name for name in cls_bases
                       if hasattr(name, 'id') and name.id == 'type'):
                return True
        # Check for the name of the first argument
        if not node.source.args or not len(node.source.args.args):
            return False
        first_arg = node.source.args.args[0]
        if first_arg.arg != 'cls':
            return False
        return True

    def get_import_violation_code(self, name, asname):
        if name == asname:
            return False
        if name.isupper():
            if not asname.isupper():
                return self.ErrorCodes.E01
        elif name.islower():
            if not asname.islower():
                return self.ErrorCodes.E02
        elif asname.islower():
            return self.ErrorCodes.E03
        else:
            return self.ErrorCodes.E04

    def check_importation(self, node):
        name = node.fullName.split('.')[-1]
        asname = node.name
        violation = namedtuple('violation', ['name', 'asname', 'error'])
        return violation(name,
                         asname,
                         self.get_import_violation_code(name, asname))

    def check_from_importation(self, node):
        name = node.real_name
        asname = node.name

        violation = namedtuple('violation', ['name', 'asname', 'error'])
        return violation(name,
                         asname,
                         self.get_import_violation_code(name, asname))

    def check_double_underscore(self, node):
        if type(node.parent) == ClassDefinition:
            return True
        if '__' in (node.name[:2], node.name[-2:]):
            return False
        return True

    def is_mixed_case(self, name):
        return name.lower() != name and name.lstrip('_')[:1].islower()

    def run(self, filename, file,
            dependency_results=dict()
            ):
        """
        Uses PyFlakesASTBear to get only FutureImportation
        """
        for result in dependency_results.get(PyFlakesASTBear.name, []):
            scopes = result.doctest_scopes
            scopes.append(result.module_scope)
            for scope in scopes:
                for importation in result.get_nodes(scope, Importation):
                    violation = self.check_importation(importation)
                    if violation.error:
                        yield Result.from_values(
                            origin=self,
                            message=violation.error.format(
                                name=violation.name, asname=violation.asname),
                            file=filename,
                            line=importation.source.lineno)

                for importation in result.get_nodes(scope, ImportationFrom):
                    violation = self.check_from_importation(importation)
                    if violation.error:
                        yield Result.from_values(
                            origin=self,
                            message=violation.error.format(
                                name=violation.name, asname=violation.asname),
                            file=filename,
                            line=importation.source.lineno)

                for class_definition in result.get_class_definitions(scope):
                    if not self.is_valid_class_name(class_definition):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E05.format(
                                name=class_definition.name),
                            file=filename,
                            line=class_definition.source.lineno)

                for function_definition in result.get_function_definitions(
                                                        scope):
                    if not self.is_valid_function_name(function_definition):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E06.format(
                                name=function_definition.name),
                            file=filename,
                            line=function_definition.source.lineno)

                    if not self.check_double_underscore(function_definition):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E07,
                            file=filename,
                            line=function_definition.source.lineno)

                    if not self.check_method_arg(function_definition):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E09,
                            file=filename,
                            line=function_definition.source.lineno)

                    if not self.check_class_method_arg(function_definition):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E10,
                            file=filename,
                            line=function_definition.source.lineno)

                for binding in result.get_nodes(scope, Binding):
                    if self.is_mixed_case(binding.name):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E12.format(
                                name=binding.name),
                            file=filename,
                            line=binding.source.lineno,
                            column=binding.source.col_offset)

                for assignment in result.get_nodes(scope,
                                                   Assignment):
                    if self.is_mixed_case(assignment.name):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E12.format(
                                name=assignment.name),
                            file=filename,
                            line=assignment.source.lineno,
                            column=assignment.source.col_offset)

            for class_scope in result.class_scopes:
                for binding in result.get_nodes(class_scope, Binding):
                    if self.is_mixed_case(binding.name):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E11.format(
                                name=binding.name),
                            file=filename,
                            line=binding.source.lineno,
                            column=binding.source.col_offset)

                for assignment in result.get_nodes(class_scope,
                                                   Assignment):
                    if self.is_mixed_case(assignment.name):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E11.format(
                                name=assignment.name),
                            file=filename,
                            line=assignment.source.lineno,
                            column=assignment.source.col_offset)

            for function_scope in result.function_scopes:
                for argument in result.get_nodes(function_scope, Argument):
                    if not argument.name.islower():
                        print(Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E08.format(
                                name=argument.name),
                            file=filename,
                            line=argument.source.lineno,
                            column=argument.source.col_offset))
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E08.format(
                                name=argument.name),
                            file=filename,
                            line=argument.source.lineno,
                            column=argument.source.col_offset)

                for binding in result.get_nodes(function_scope, Binding):
                    if not(binding.name.islower() or binding.name == '_'):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E13.format(
                                name=binding.name),
                            file=filename,
                            line=binding.source.lineno,
                            column=binding.source.col_offset)

                for assignment in result.get_nodes(function_scope,
                                                   Assignment):
                    name = assignment.name
                    if not(name.islower() or name == '_'):
                        yield Result.from_values(
                            origin=self,
                            message=self.ErrorCodes.E13.format(
                                name=assignment.name),
                            file=filename,
                            line=assignment.source.lineno,
                            column=assignment.source.col_offset)
