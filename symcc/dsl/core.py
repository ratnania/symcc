# coding: utf-8

import os
from sympy import Symbol, sympify
from symcc.dsl.utilities import grad, d_var, inner, outer, cross, dot
from textx.metamodel import metamodel_from_str

__all__ = ["Basic", "Parser", "Codegen"]

# Global variable namespace
namespace = {}
stack = {}


class Basic(object):
    def __init__(self, declarations=None, statements=None):
        self.declarations = declarations
        self.statements   = statements


class Parser(object):
    def __init__(self, grammar=None, filename=None, \
                 classes=None):

        _grammar = grammar

        # ... read the grammar from a file
        if not (filename is None):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir_path, filename)

            f = open(filename)
            _grammar = f.read()
            _grammar.replace("\n", "")
            f.close()
        # ...

        # ...
        self.grammar = _grammar
        # ...

        # ...
        if classes is None:
            self.model = metamodel_from_str(_grammar)
        else:
            self.model = metamodel_from_str(_grammar, classes=classes)
        # ...

    def parse(self, instructions):
        # ... parse the DSL code
        return self.model.model_from_str(instructions)
        # ...

    def parse_from_file(self, filename):
        # ... read a DSL code
        f = open(filename)
        instructions = f.read()
        instructions.replace("\n", "")
        f.close()
        # ...

        # ... parse the DSL code
        return self.parse(instructions)
        # ...


class Codegen(object):
    def __init__(self, body, local_vars=None, args=None):

        self._body = body

        self._local_vars = local_vars
        if local_vars is None:
            self._local_vars = []

        self._args = args
        if args is None:
            self._args = []

    @property
    def body(self):
        return self._body

    @property
    def local_vars(self):
        return self._local_vars

    @property
    def args(self):
        return self._args
