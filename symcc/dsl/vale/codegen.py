# coding: utf-8
from symcc.types.ast import For, Assign
from symcc.utilities.codegen import codegen, Result

from sympy.core.symbol import Symbol
from sympy.abc import x,y,i
from sympy.tensor import Idx, Indexed, IndexedBase
from sympy.core.sympify import sympify

__all__ = ["ValeCodegen"]


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



class Pullback(Codegen):
    def __init__(self, dim, trial=False):
        Ni_u  = Symbol('Ni_u')
        Ni_v  = Symbol('Ni_v')
        Ni_w  = Symbol('Ni_w')

        Ni_x  = Symbol('Ni_x')
        Ni_y  = Symbol('Ni_y')
        Ni_z  = Symbol('Ni_z')

        if trial:
            Nj_u  = Symbol('Nj_u')
            Nj_v  = Symbol('Nj_v')
            Nj_w  = Symbol('Nj_w')

            Nj_x  = Symbol('Nj_x')
            Nj_y  = Symbol('Nj_y')
            Nj_z  = Symbol('Nj_z')

        body  = []
        body += [Assign(Ni_x,Ni_u), Assign(Ni_y,Ni_v), Assign(Ni_z,Ni_w)][:dim]
        if trial:
            body += [Assign(Nj_x,Nj_u), Assign(Nj_y,Nj_v), Assign(Nj_z,Nj_w)][:dim]

        local_vars  = []

        local_vars += [Ni_u, Ni_v, Ni_w][:dim]
        local_vars += [Ni_x, Ni_y, Ni_z][:dim]

        if trial:
            local_vars += [Nj_u, Nj_v, Nj_w][:dim]
            local_vars += [Nj_x, Nj_y, Nj_z][:dim]

        super(Pullback, self).__init__(body, local_vars=local_vars)


class Geometry(Codegen):
    def __init__(self, dim):
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_x = IndexedBase('arr_x')
        arr_y = IndexedBase('arr_y')
        arr_z = IndexedBase('arr_z')

        arr_wvol = IndexedBase('arr_wvol')

        args  = [n1, n2, n3][:dim]
        args += [arr_wvol]
        args += [arr_x, arr_y, arr_z][:dim]
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        x  = Symbol('x')
        y  = Symbol('y')
        z  = Symbol('z')

        wvol  = Symbol('wvol')

        local_vars  = [wvol]

        local_vars += [ x,  y,  z][:dim]
        # ...

        # ...
        body = []
        if dim == 1:
            body.append(Assign(x, arr_x[g1]))

            body.append(Assign(wvol, arr_wvol[g1]))
        if dim == 2:
            g = Idx('g', n1 * n2)
            body.append(Assign(g, sympify('(g2-1)*n1 + g1')))

            body.append(Assign(x, arr_x[g]))
            body.append(Assign(y, arr_y[g]))

            body.append(Assign(wvol, arr_wvol[g]))
        if dim == 3:
            g = Idx('g', n1 * n2 * n3)
            body.append(Assign(g, sympify('(g3-1)*n2*n1 + (g2-1)*n1 + g1')))

            body.append(Assign(x, arr_x[g]))
            body.append(Assign(y, arr_y[g]))
            body.append(Assign(z, arr_z[g]))

            body.append(Assign(wvol, arr_wvol[g]))
        # ...

        super(Geometry, self).__init__(body, local_vars=local_vars, args=args)


class TestFunction(Codegen):
    def __init__(self, dim):
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_Ni1_0 = IndexedBase('arr_Ni1_0')
        arr_Ni2_0 = IndexedBase('arr_Ni2_0')
        arr_Ni3_0 = IndexedBase('arr_Ni3_0')

        arr_Ni1_s = IndexedBase('arr_Ni1_s')
        arr_Ni2_s = IndexedBase('arr_Ni2_s')
        arr_Ni3_s = IndexedBase('arr_Ni3_s')

        args  = []
        args += [n1, n2, n3][:dim]
        args += [arr_Ni1_0, arr_Ni2_0, arr_Ni3_0][:dim]
        args += [arr_Ni1_s, arr_Ni2_s, arr_Ni3_s][:dim]
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        Ni_0  = Symbol('Ni_0')
        Ni_u  = Symbol('Ni_u')
        Ni_v  = Symbol('Ni_v')
        Ni_w  = Symbol('Ni_w')

        local_vars  = [Ni_0]

        local_vars += [Ni_u, Ni_v, Ni_w][:dim]
        # ...

        # ...
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
        # ...

        super(TestFunction, self).__init__(body, local_vars=local_vars, args=args)


class TrialFunction(Codegen):
    def __init__(self, dim):
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_Nj1_0 = IndexedBase('arr_Nj1_0')
        arr_Nj2_0 = IndexedBase('arr_Nj2_0')
        arr_Nj3_0 = IndexedBase('arr_Nj3_0')

        arr_Nj1_s = IndexedBase('arr_Nj1_s')
        arr_Nj2_s = IndexedBase('arr_Nj2_s')
        arr_Nj3_s = IndexedBase('arr_Nj3_s')

        args  = []
        args += [n1, n2, n3][:dim]
        args += [arr_Nj1_0, arr_Nj2_0, arr_Nj3_0][:dim]
        args += [arr_Nj1_s, arr_Nj2_s, arr_Nj3_s][:dim]
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        Nj_0  = Symbol('Nj_0')
        Nj_u  = Symbol('Nj_u')
        Nj_v  = Symbol('Nj_v')
        Nj_w  = Symbol('Nj_w')

        local_vars  = [Nj_0]

        local_vars += [Nj_u, Nj_v, Nj_w][:dim]
        # ...

        # ...
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
        # ...

        super(TrialFunction, self).__init__(body, local_vars=local_vars, args=args)


class Formulation(Codegen):
    def __init__(self, expr):
        contribution = Symbol("contribution")
        wvol = Symbol("wvol")

        body       = [Assign(contribution, contribution + expr * wvol)]
        local_vars = []
        args       = [contribution]

        super(Formulation, self).__init__(body, local_vars=local_vars, args=args)


class ValeCodegen(Codegen):
    """Code generation for the Vale Grammar"""
    def __init__(self, expr, dim=None, name=None, trial=False, ast=None):
        """
        expr: sympy.expression or LinearForm or BilinearForm
            if expr is a LinearForm or BilinearForm, then either dim or ast must
            be provided.
        """
        from symcc.dsl.vale import LinearForm, BilinearForm

        _expr   = None
        _name   = None
        _dim    = None
        _trial  = False
        _n_rows = None
        _n_cols = None

        if isinstance(expr, LinearForm):
            _expr = expr.to_sympy()
            for f in expr.args.functions:
                B = "Ni"
                _expr = _expr.subs({Symbol(f): Symbol(B + "_0")})
                for d in ["x", "y", "z"][:_dim]:
                    _expr = _expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})

            _name = "kernel_" + expr.name
            _dim  = expr.attributs["dim"]

            # TODO get n_rows from LinearForm
            _n_rows = Symbol('n_rows', integer=True)

        elif isinstance(expr, BilinearForm):
            _expr = expr.to_sympy()
            for f in expr.args_test.functions:
                B = "Ni"
                _expr = _expr.subs({Symbol(f): Symbol(B + "_0")})
                for d in ["x", "y", "z"][:_dim]:
                    _expr = _expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})

            for f in expr.args_trial.functions:
                B = "Nj"
                _expr = _expr.subs({Symbol(f): Symbol(B + "_0")})
                for d in ["x", "y", "z"][:_dim]:
                    _expr = _expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})

            _name  = "kernel_" + expr.name
            _dim   = expr.attributs["dim"]
            _trial = True

            # TODO get n_rows,n_cols from BilinearForm
            _n_rows = Symbol('n_rows', integer=True)
            _n_cols = Symbol('n_cols', integer=True)

        else:
            if not(dim is None) or not(name is None):
                raise ValueError("Both dim and name must be provided.")

            _expr  = expr
            _name  = name
            _dim   = dim
            _trial = trial

        self._name = _name

        stmts  = []
        stmts += [Geometry(_dim), \
                  TestFunction(_dim)]
        if _trial:
            stmts += [TrialFunction(_dim)]

        stmts += [Pullback(_dim, trial=_trial), \
                  Formulation(_expr)]

        body       = []
        local_vars = []
        args       = []

        if not(_n_rows is None):
            args.append(_n_rows)

        if not(_n_cols is None):
            args.append(_n_cols)

        for stmt in stmts:
            if isinstance(stmt, Codegen):
                body       += stmt.body
                local_vars += stmt.local_vars
                args       += stmt.args
            elif isinstance(stmt, For):
                body       += stmt.body
                local_vars += stmt.target
                args       += stmt.iterable.stop
            else:
                raise ValueError("Unknown statement : %s" % stmt)

        contribution = Symbol("contribution")

        g1 = Symbol('g1', integer=True)
        n1 = Symbol('n1', integer=True)

        g2 = Symbol('g2', integer=True)
        n2 = Symbol('n2', integer=True)

        g3 = Symbol('g3', integer=True)
        n3 = Symbol('n3', integer=True)

        if _dim >= 3:
            body = [For(g3, (1, n3, 1), body)]
        if _dim >= 2:
            body = [For(g2, (1, n2, 1), body)]
        body  = [Assign(contribution, 0.), For(g1, (1, n1, 1), body)]

        super(ValeCodegen, self).__init__(body, \
                                            local_vars=local_vars, \
                                            args=args)

    @property
    def name(self):
        return self._name

    def doprint(self, language):
        args        = self.args
        local_vars  = self.local_vars
        return_vars = []
        if language in ["LUA"]:
            args.remove(Symbol("contribution"))
            local_vars.append(Symbol("contribution"))
            return_vars.append(Result(Symbol("contribution")))

            [(f_name, f_code)] = codegen((self.name, self.body), language, \
                                         header=False, empty=True, \
                                         argument_sequence=set(args), \
                                         local_vars=set(local_vars), \
                                         return_vars=return_vars)
        else:
            [(f_name, f_code), header] = codegen((self.name, self.body), language, \
                                                 header=False, empty=True, \
                                                 argument_sequence=set(args), \
                                                 local_vars=set(local_vars), \
                                                 return_vars=return_vars)

        return f_code

