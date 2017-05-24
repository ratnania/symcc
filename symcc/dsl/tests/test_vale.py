# coding: utf-8

from symcc.printers import fcode
from symcc.dsl.codegen import ValeCodegen
from symcc.dsl.vale import ValeParser

from sympy import S
from sympy.core.sympify import sympify


def test_vale():
    dim = 2

    expr = sympify("Ni_x*Nj_x")
    kernel = ValeCodegen(expr, dim, name="kernel", trial=True)
    print (kernel.doprint("F95"))


def test_dsl():

    # ... creates an instance of Vale parser
    vale = ValeParser()
    # ...

    # ... parse the Vale code
    ast = vale.parse_from_file("vale/test.vl")
    # ...

    # ... for every token, we print its name and type
    for token in ast.declarations:
        print token.name, type(token)
    # ...

    # ...
    # construct the list of all declarations
    identifiers = [token.name for token in ast.declarations]
    # ...

    # ...
    def get_by_name(ast, name):
        """
        Returns an object from the AST by giving its name.
        """
        for token in ast.declarations:
            if token.name == name:
                return token
        return None
    # ...

    # ...
    f  = get_by_name(ast, "f")
    l1 = get_by_name(ast, "l1")
    a1 = get_by_name(ast, "a1")
    # ...

    # ... TODO get dim from domain
    dim = 3
    kernel = ValeCodegen(a1, dim, name="kernel", trial=True)
#    print (kernel.doprint("F95"))
    print (kernel.doprint("LUA"))
    # ...

######################################
if __name__ == "__main__":
    test_dsl()
#    test_vale()
