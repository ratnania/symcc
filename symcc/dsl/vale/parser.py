# coding: utf-8

from sympy import Symbol, sympify

from symcc.dsl.utilities import grad, d_var, inner, outer, cross, dot
from symcc.dsl.core import Basic, Parser
from symcc.dsl.vale.syntax import (Vale, \
                                   Expression, Term, Operand, \
                                   FactorSigned, FactorUnary, FactorBinary, \
                                   LinearForm, BilinearForm, \
                                   Domain, Space, Field, Function, Real)


__all__ = ["ValeParser", "ast_to_dict"]

# ...
def _get_by_name(ast, name):
    """
    Returns an object from the AST by giving its name.
    """
    for token in ast.declarations:
        if token.name == name:
            return token
    return None
# ...

# ...
def ast_to_dict(ast):
    """
    Returns an object from the AST by giving its name.
    """
    tokens = {}
    for token in ast.declarations:
        tokens[token.name] = token
    return tokens
# ...

# User friendly parser

class ValeParser(Parser):
    def __init__(self, filename=None):
        classes = [Vale, \
                   Expression, Term, Operand, \
                   FactorSigned, FactorUnary, FactorBinary, \
                   LinearForm, BilinearForm, \
                   Domain, Space, Field, Function, Real \
                   ]

        if filename is None:
            filename = "vale/grammar.tx"

        super(ValeParser, self).__init__(filename = filename, \
                                         classes=classes)

    def parse_from_file(self, filename):
        ast = super(ValeParser, self).parse_from_file(filename)

        # ... annotating the AST
        for token in ast.declarations:
            if isinstance(token, LinearForm):
                user_fields    = []
                user_functions = []
                user_constants = []

                space  = _get_by_name(ast, token.args.space)
                domain = _get_by_name(ast, space.domain)

                expr = token.to_sympy()
                free_symbols = expr.free_symbols
                for symbol in free_symbols:
                    var = _get_by_name(ast, str(symbol))
                    if isinstance(var, Field):
                        user_fields.append(var.name)
                    elif isinstance(var, Function):
                        user_functions.append(var.name)
                    elif isinstance(var, Real):
                        user_constants.append(var.name)

                token.set("dim", domain.dim)
                token.set("user_fields", user_fields)
                token.set("user_functions", user_functions)
                token.set("user_constants", user_constants)

#                print("> FIELDS    : " + str(token.attributs["user_fields"]))
#                print("> FUNCTIONS : " + str(token.attributs["user_functions"]))
#                print("> CONSTANTS : " + str(token.attributs["user_constants"]))

            elif isinstance(token, BilinearForm):
                user_fields    = []
                user_functions = []
                user_constants = []

                space_test  = _get_by_name(ast, token.args_test.space)
                space_trial = _get_by_name(ast, token.args_trial.space)
                domain      = _get_by_name(ast, space_test.domain)

                expr = token.to_sympy()
                free_symbols = expr.free_symbols
                for symbol in free_symbols:
                    var = _get_by_name(ast, str(symbol))
                    if isinstance(var, Field):
                        user_fields.append(var.name)
                    elif isinstance(var, Function):
                        user_functions.append(var.name)
                    elif isinstance(var, Real):
                        user_constants.append(var.name)

                token.set("dim", domain.dim)
                token.set("user_fields", user_fields)
                token.set("user_functions", user_functions)
                token.set("user_constants", user_constants)

#                print("> FIELDS    : " + str(token.attributs["user_fields"]))
#                print("> FUNCTIONS : " + str(token.attributs["user_functions"]))
#                print("> CONSTANTS : " + str(token.attributs["user_constants"]))
        # ...

        return ast
