# coding: utf-8

import os
from textx.metamodel import metamodel_from_str

__all__ = ["Codegen"]




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
