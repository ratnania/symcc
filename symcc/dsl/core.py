# coding: utf-8

import os
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
    """ Class for a Parser using TextX.

    A parser can be created from a grammar (str) or a filename. It is preferable
    to specify the list classes to have more control over the abstract grammar;
    for example, to use a namespace, and to do some specific anotation.

    >>> parser = Parser(filename="vale/gammar.tx")

    Once the parser is created, you can parse a given set of instructions by
    calling

    >>> parser.parse(["Field(V) :: u"])

    or by providing a file to parse

    >>> parser.parse_from_file("vale/tests/inputs/1d/poisson.vl")
    """
    def __init__(self, grammar=None, filename=None, \
                 classes=None):
        """Parser constructor.

        grammar : str
            abstract grammar describing the DSL.

        filename: str
            name of the file containing the abstract grammar.

        classes : list
            a list of Python classes to be used to describe the grammar. Take a
            look at TextX documentation for more details.
        """

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
        """Parse a set of instructions with respect to the grammar.

        instructions: list
            list of instructions to parse.
        """
        # ... parse the DSL code
        return self.model.model_from_str(instructions)
        # ...

    def parse_from_file(self, filename):
        """Parse a set of instructions with respect to the grammar.

        filename: str
            a file containing the instructions to parse.
        """
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
    """Abstract class for code generation.

    A code generation class must provide

    * body: a list of statements
    * args: arguments for the body
    * local_vars: variables that are local and do not appear in args

    A Codegen class can be described by a function or procedure, depending on
    the backend languages.

    """
    def __init__(self, body, local_vars=None, args=None):
        """Constructor for the Codegen class.

        body: list
            list of statements.

        local_vars: list
            list of local variables.

        args: list
            list of arguments.
        """

        self._body = body

        self._local_vars = local_vars
        if local_vars is None:
            self._local_vars = []

        self._args = args
        if args is None:
            self._args = []

    @property
    def body(self):
        """Returns the body of the Codegen class"""
        return self._body

    @property
    def local_vars(self):
        """Returns the local variables of the Codegen class"""
        return self._local_vars

    @property
    def args(self):
        """Returns the arguments of the Codegen class"""
        return self._args
