# coding: utf-8

from symcc.dsl.vale import ValeParser


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

######################################
if __name__ == "__main__":
    test_dsl()
