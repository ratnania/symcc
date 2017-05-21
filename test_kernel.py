# coding: utf-8
from sympy.core.symbol import Symbol
from sympy import Eq as Assign
from symcc.types.ast import For
#from symcc.types.ast import Assign
from sympy.abc import x,y,i
from sympy.tensor import Idx, Indexed, IndexedBase

from sympy.core.sympify import sympify


# ...
def prelude_testfunction(dim):
    n1 = Symbol('n1', integer=True)
    n2 = Symbol('n2', integer=True)
    n3 = Symbol('n3', integer=True)

    g1 = Idx('g1', n1)
    g2 = Idx('g2', n2)
    g3 = Idx('g3', n3)

    arr_Ni1_0 = IndexedBase('arr_Ni1_0')
    arr_Ni2_0 = IndexedBase('arr_Ni2_0')
    arr_Ni3_0 = IndexedBase('arr_Ni3_0')

    arr_Ni1_s = IndexedBase('arr_Ni1_s')
    arr_Ni2_s = IndexedBase('arr_Ni2_s')
    arr_Ni3_s = IndexedBase('arr_Ni3_s')

    Ni_0  = Symbol('Ni_0')
    Ni_u  = Symbol('Ni_u')
    Ni_v  = Symbol('Ni_v')
    Ni_w  = Symbol('Ni_w')

    body = []

    if dim == 1:
        body.append(Assign(Ni_0, arr_Ni1_0[g1]))
        body.append(Assign(Ni_u, arr_Ni1_s[g1]))
    if dim == 2:
        body.append(Assign(Ni_0, arr_Ni1_0[g1] * arr_Ni2_0[g2]))
        body.append(Assign(Ni_u, arr_Ni1_s[g1] * arr_Ni2_0[g2]))
        body.append(Assign(Ni_v, arr_Ni1_0[g1] * arr_Ni2_s[g2]))
    if dim == 3:
        body.append(Assign(Ni_0, arr_Ni1_0[g1] * arr_Ni2_0[g2] * arr_Ni3_0[g3]))
        body.append(Assign(Ni_u, arr_Ni1_s[g1] * arr_Ni2_0[g2] * arr_Ni3_0[g3]))
        body.append(Assign(Ni_v, arr_Ni1_0[g1] * arr_Ni2_s[g2] * arr_Ni3_0[g3]))
        body.append(Assign(Ni_w, arr_Ni1_0[g1] * arr_Ni2_0[g2] * arr_Ni3_s[g3]))

    return body
# ...

# ...
def prelude_trialfunction(dim):
    n1 = Symbol('n1', integer=True)
    n2 = Symbol('n2', integer=True)
    n3 = Symbol('n3', integer=True)

    g1 = Idx('g1', n1)
    g2 = Idx('g2', n2)
    g3 = Idx('g3', n3)

    arr_Nj1_0 = IndexedBase('arr_Nj1_0')
    arr_Nj2_0 = IndexedBase('arr_Nj2_0')
    arr_Nj3_0 = IndexedBase('arr_Nj3_0')

    arr_Nj1_s = IndexedBase('arr_Nj1_s')
    arr_Nj2_s = IndexedBase('arr_Nj2_s')
    arr_Nj3_s = IndexedBase('arr_Nj3_s')

    Nj_0  = Symbol('Nj_0')
    Nj_u  = Symbol('Nj_u')
    Nj_v  = Symbol('Nj_v')
    Nj_w  = Symbol('Nj_w')

    body = []

    if dim == 1:
        body.append(Assign(Nj_0, arr_Nj1_0[g1]))
        body.append(Assign(Nj_u, arr_Nj1_s[g1]))
    if dim == 2:
        body.append(Assign(Nj_0, arr_Nj1_0[g1] * arr_Nj2_0[g2]))
        body.append(Assign(Nj_u, arr_Nj1_s[g1] * arr_Nj2_0[g2]))
        body.append(Assign(Nj_v, arr_Nj1_0[g1] * arr_Nj2_s[g2]))
    if dim == 3:
        body.append(Assign(Nj_0, arr_Nj1_0[g1] * arr_Nj2_0[g2] * arr_Nj3_0[g3]))
        body.append(Assign(Nj_u, arr_Nj1_s[g1] * arr_Nj2_0[g2] * arr_Nj3_0[g3]))
        body.append(Assign(Nj_v, arr_Nj1_0[g1] * arr_Nj2_s[g2] * arr_Nj3_0[g3]))
        body.append(Assign(Nj_w, arr_Nj1_0[g1] * arr_Nj2_0[g2] * arr_Nj3_s[g3]))

    return body
# ...


# ...
def build_weak_formulation(contribution, expr):
    contribution = Symbol("contribution")
    wvol = Symbol("wvol")

    rhs = contribution + expr * wvol

    return Assign(contribution, rhs)
# ...

# ...
def kernel(dim, expr=None):
    main = None
    contribution = Symbol("contribution")

    body = []

#    body  = prelude_geometry(dim)
#    body += prelude_testfunction(dim)
#    body += prelude_trialfunction(dim)
    body += prelude_pullback(dim)
#    if expr is not None:
#        body += [build_weak_formulation(contribution, expr)]

    g1 = Symbol('g1', integer=True)
    n1 = Symbol('n1', integer=True)

    g2 = Symbol('g2', integer=True)
    n2 = Symbol('n2', integer=True)

    g3 = Symbol('g3', integer=True)
    n3 = Symbol('n3', integer=True)

#    if dim >= 3:
#        body = [For(g3, (1, n3, 1), body)]
#    if dim >= 2:
#        body = [For(g2, (1, n2, 1), body)]
#
#    main = For(g1, (1, n1, 1), body)


    main = body
    return main
# ...




class Basic(object):
    def __init__(self, body, local_vars=None, args=None):

        self._body = body

        self._local_vars = local_vars
        if local_vars is None:
            self._local_vars = set([])

        self._args = args
        if args is None:
            self._args = set([])

    @property
    def body(self):
        return self._body

    @property
    def local_vars(self):
        return self._local_vars

    @property
    def args(self):
        return self._args


class Pullback(Basic):
    def __init__(self, dim):
        Ni_u  = Symbol('Ni_u')
        Ni_v  = Symbol('Ni_v')
        Ni_w  = Symbol('Ni_w')

        Ni_x  = Symbol('Ni_x')
        Ni_y  = Symbol('Ni_y')
        Ni_z  = Symbol('Ni_z')

        Nj_u  = Symbol('Nj_u')
        Nj_v  = Symbol('Nj_v')
        Nj_w  = Symbol('Nj_w')

        Nj_x  = Symbol('Nj_x')
        Nj_y  = Symbol('Nj_y')
        Nj_z  = Symbol('Nj_z')

        body = set([Assign(Nj_x,Nj_u), Assign(Nj_y,Nj_v), Assign(Nj_z,Nj_w)][:dim])

        local_vars  = set([])

        local_vars = local_vars.union(set([Ni_u, Ni_v, Ni_w][:dim]))
        local_vars = local_vars.union(set([Ni_x, Ni_y, Ni_z][:dim]))

        local_vars = local_vars.union(set([Nj_u, Nj_v, Nj_w][:dim]))
        local_vars = local_vars.union(set([Nj_x, Nj_y, Nj_z][:dim]))

        super(Pullback, self).__init__(body, local_vars=local_vars)


class Geometry(Basic):
    def __init__(self, dim):
        # ...
        arr_x = IndexedBase('arr_x')
        arr_y = IndexedBase('arr_y')
        arr_z = IndexedBase('arr_z')

        arr_wvol = IndexedBase('arr_wvol')

        args = set([arr_wvol])
        args = args.union(set([arr_x, arr_y, arr_z][:dim]))
        # ...

        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        x  = Symbol('x')
        y  = Symbol('y')
        z  = Symbol('z')

        wvol  = Symbol('wvol')

        local_vars  = set([wvol])

        local_vars = local_vars.union(set([n1, n2, n3][:dim]))
        local_vars = local_vars.union(set([g1, g2, g3][:dim]))
        local_vars = local_vars.union(set([ x,  y,  z][:dim]))
        # ...

        # ...
        body = set([])
        if dim == 1:
            body.add(Assign(x, arr_x[g1]))

            body.add(Assign(wvol, arr_wvol[g1]))
        if dim == 2:
            body.add(Assign(Symbol('g'), sympify('(g2-1)*n1 + g1')))

            g = Idx('g', n1 * n2)
            body.add(Assign(x, arr_x[g]))
            body.add(Assign(y, arr_y[g]))

            body.add(Assign(wvol, arr_wvol[g]))
        if dim == 3:
            body.add(Assign(Symbol('g'), sympify('(g3-1)*n2*n1 + (g2-1)*n1 + g1')))

            g = Idx('g', n1 * n2 * n3)
            body.add(Assign(x, arr_x[g]))
            body.add(Assign(y, arr_y[g]))
            body.add(Assign(z, arr_z[g]))

            body.add(Assign(wvol, arr_wvol[g]))
        # ...

        super(Geometry, self).__init__(body, local_vars=local_vars, args=args)


# ...
def prelude_geometry(dim):
    body = []


    return body
# ...

########################################
if __name__ == "__main__":
    from symcc.printers import fcode # not working with Assign
    from symcc.utilities.codegen import codegen
    from symcc.types.ast import Assign
    from sympy import S

    dim = 1

    expr = sympify("Ni_x*Nj_x")

    stmts  = []
    stmts += [Pullback(dim), Geometry(dim)]

    body       = set([])
    local_vars = set([])
    args       = set([])

    for stmt in stmts:
        body = body.union(stmt.body)
        local_vars = local_vars.union(stmt.local_vars)
        args = args.union(stmt.args)

#    body += [Assign(contribution, S.Zero)]
#    body  = prelude_geometry(dim)
#    body += prelude_testfunction(dim)
#    body += prelude_trialfunction(dim)

    g1 = Symbol('g1', integer=True)
    n1 = Symbol('n1', integer=True)

    body  = For(g1, (1, n1, 1), body)

    local_vars = local_vars.union({ g1, n1 })

    [(f_name, f_code), header] = codegen(("kernel", body), "F95", \
                                         header=False, empty=True, \
                                         argument_sequence=args, \
                                         local_vars=local_vars)

    print(f_code)



#
#    dim = 1
#
##    expr = sympify("Ni_x*Nj_x + Ni_y*Nj_y")
#    expr = sympify("Ni_x*Nj_x")
#
#    wvol = Symbol("wvol")
#    contribution = Symbol("contribution")
#
#    Ni_u  = Symbol('Ni_u')
#    Ni_x  = Symbol('Ni_x')
#    Nj_u  = Symbol('Nj_u')
#    Nj_x  = Symbol('Nj_x')
#
#    body  = []
#    body += [Assign(contribution, S.Zero)]
#    body += kernel(dim, expr=expr)
#
#    local_vars = { Ni_u, Ni_x, Nj_u, Nj_x, wvol, contribution }
#
#    [(f_name, f_code), header] = codegen(("kernel", body), "F95", \
#                                         header=False, empty=True, \
#                                         argument_sequence=(contribution, ), \
#                                         local_vars=local_vars)
#
#    print(f_code)
