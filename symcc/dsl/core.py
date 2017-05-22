# coding: utf-8

import os
from sympy import Symbol, sympify
from symcc.dsl.utilities import grad, d_var, inner, outer, cross, dot
from textx.metamodel import metamodel_from_str

# Global variable namespace
namespace = {}
stack = {}


class Basic(object):
    def __init__(self, declarations=None, statements=None):
        self.declarations = declarations
        self.statements   = statements

    @classmethod
    def parse(cls, instructions):
        print("BONJOUR")

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
