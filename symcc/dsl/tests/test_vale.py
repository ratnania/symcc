# coding: utf-8

from textx.metamodel import metamodel_from_str
from symcc.dsl.vale import (Domain, Space, Field, Function, Real, \
                            LinearForm, BilinearForm, \
                            FactorSigned, FactorUnary, FactorBinary, \
                            Expression, Term, Operand, \
                            Vale)


def test_dsl():
    # ... read the grammar
    filename = "../grammar/vale.tx"
    f = open(filename)
    grammar = f.read()
    grammar.replace("\n", "")
    f.close()
    # ...

    # ... create metamodel from the grammar
    builtin = [Domain, Space, Field, Function, Real]
    forms   = [LinearForm, BilinearForm]
    factors = [FactorSigned, FactorUnary, FactorBinary]
    expressions = [Expression, Term, Operand] + factors + forms

    classes = [Vale] + expressions + builtin
    mm = metamodel_from_str(grammar,
                            classes=classes)
    # ...


    # ... read a Vale code
    filename = "vale/test.vl"
    f = open(filename)
    instructions = f.read()
    instructions.replace("\n", "")
    f.close()
    # ...

    # ... parse the Vale code
    ast = mm.model_from_str(instructions)
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

######################################
if __name__ == "__main__":
    test_dsl()
