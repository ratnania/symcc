# coding: utf-8

from symcc.dsl.vale import ValeCodegen
from symcc.dsl.vale import ValeParser
from symcc.dsl.vale import construct_model

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
    ast = vale.parse_from_file("inputs/example_1.vl")
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
    l = get_by_name(ast, "l")
    a = get_by_name(ast, "a")
    # ...

    # ... TODO get dim from domain
    for f in [l, a]:
        print("============ " + f.name + " ============")
        kernel = ValeCodegen(f)

#        print (kernel.doprint("F95"))
        print (kernel.doprint("LUA"))
    # ...

def test_model():

    # ...
    def run(filename):
        # ...
        from caid.cad_geometry import square
        geometry = square()

        from clapp.spl.mapping import Mapping
        mapping = Mapping(geometry=geometry)
        # ...

        # ...
        import os

        cmd = "mkdir -p output"
        os.system(cmd)
        # ...

        # ... creates discretization parameters
        from clapp.disco.parameters.bspline import BSpline

        bspline_params = BSpline([8,8], [2,2], \
                                 bc_min=[0,0], \
                                 bc_max=[0,0])
        # ...

        # ... create a context from discretization
        from clapp.fema.context        import Context

        context = Context(dirname="input", \
                          discretization_params=bspline_params)
        # ...

        # ...
        pde = construct_model(filename, backend="clapp", \
                              context=context, mapping=mapping)
        # ...

        # ... accessing the pde declarations
        V           = pde["V"]
        u           = pde["u"]
        form_a      = pde["a"]
        form_b      = pde["b"]
        # ...

        # ...
#        assembler_a = form_a.assembler
#        matrix      = form_a.matrix
        assembler_b = form_b.assembler
        rhs         = form_b.vector

#        assembler_a.assemble()
        assembler_b.assemble()
        # ...

        # ...
        rhs.export("rhs.txt")
        # ...
    # ...

    run(filename="inputs/example_1.vl")

######################################
if __name__ == "__main__":
#    test_vale()
#    test_dsl()
    test_model()
