from .parser import parse
from .constants import *
import traceback, sys


class Interpreter(object):
    def __int__(self, ast):
        self.reset()

    def reset(self):
        self.vars = {}
        self.it = None

    def interpret(self, ast):
        self.reset()
        self.process_statements(ast)

    def process_statements(self, statements):
        if not len(statements):
          raise Exception("LOSE WHILE PARSE PROGRAM. MAEK SHUR U TYPE \"HAI\" AN \"KTHXBYE\" CORREKT.")
        for statement in statements:
            node_type, value = statement
            if node_type == EXPR:
                self.process_expr(value)
            if node_type == VISIBLE:
                self.process_visible(value)
            if node_type == GIMMEH:
                self.process_gimmeh(value)
            if node_type == ASSIGN:
                self.process_assign(value)
            if node_type == DECLARE:
                self.process_decl(value)
            if node_type == CAST:
                self.process_cast(value)
            if node_type == IF_ELSE:
                self.process_if_else(value)
            if node_type == LOOP:
                self.process_loop(value)

    def expr_res(self, res):
        self.it = res
        return res

    def process_expr(self, expr):
        node_type, value = expr
        if node_type == VALUE:
            return self.expr_res(self.process_value(value))
        if node_type == VAR:
            return self.expr_res(self.process_variable(value))
        if node_type in [SIZE, ABSLUT]:
          return self.expr_res(self.process_unary(node_type, value))
        if node_type in [SUM, DIFF, PRODUKT, QUOSHUNT, MOD, BIGGR, SMALLR]:
            return self.expr_res(self.process_math_expr(node_type, value))
        if node_type in [BOTH, EITHER, WON, NOT, ALL, ANY]:
            return self.expr_res(self.process_logic_expr(node_type, value))
        if node_type in [SAME, DIFFRINT]:
            return self.expr_res(self.process_equality(node_type, value))
        if node_type == SMOOSH:
            return self.expr_res(self.process_smoosh(value))
        if node_type == MAEK:
            return self.expr_res(self.process_expr_cast(value))

    def process_value(self, val):
        node_type, value = val
        if node_type == YARN:
            return value
        if node_type == NUMBR:
            return int(value)
        if node_type == NUMBAR:
            return float(value)
        if node_type == TROOF:
            if value == WIN:
                return True
            elif value == FAIL:
                return False
            else:
                raise Exception('unknown value for TROOF type')

    def get_var(self, var_name):
        if var_name in self.vars:
            return self.vars[var_name]

        raise Exception('variable {}: used before declaration'.format(var_name))

    def process_variable(self, var_name):
        if var_name == 'IT':
            return self.it

        return self.get_var(var_name)

    def process_math_expr(self, op, args):
        lhs = self.process_expr(args[0][1])
        rhs = self.process_expr(args[1][1])

        if op == SUM:
            return lhs + rhs
        if op == DIFF:
            return lhs - rhs
        if op == PRODUKT:
            return lhs * rhs
        if op == QUOSHUNT:
            return lhs / rhs
        if op == MOD:
            return lhs % rhs
        if op == BIGGR:
            return max(lhs, rhs)
        if op == SMALLR:
            return min(lhs, rhs)

    def process_logic_expr(self, op, args):
        if op in [BOTH, EITHER, WON]:
            lhs = self.process_expr(args[0][1])
            rhs = self.process_expr(args[1][1])

            if op == BOTH:
                return lhs and rhs
            if op == EITHER:
                return lhs or rhs
            if op == WON:
                return bool(lhs) ^ bool(rhs)
        if op == NOT:
            lhs = self.process_expr(args[1])
            return not lhs
        if op == ALL or op == ANY:
            exprs = [self.process_expr(arg[1]) for arg in args]

            if op == ALL:
                return all(exprs)
            if op == ANY:
                return any(exprs)

    def process_equality(self, op, args):
        lhs = self.process_expr(args[0][1])
        rhs = self.process_expr(args[1][1])

        if op == SAME:
            return lhs == rhs
        if op == DIFFRINT:
            return lhs != rhs

    def process_smoosh(self, args):
        str_args = ''.join([str(self.process_expr(arg[1])) for arg in args])
        return str_args

    def totype(self, t, val):
        if t == YARN:
            return str(val)
        if t == NUMBR:
            return int(val)
        if t == NUMBAR:
            return float(val)
        if t == TROOF:
            return bool(val)

    def process_expr_cast(self, args):
        lhs = self.process_expr(args[0][1])
        t = args[1]

        return self.totype(t, lhs)

    def process_visible(self, args):
        to_print, new_line = args
        to_print = ''.join([str(self.process_expr(arg[1])) for arg in to_print])

        print(to_print, end='\n' if new_line else '')

    def process_unary(self, expr, obj):
      if expr == SIZE:
        return len(self.process_expr(obj[1]))
      elif expr == ABSLUT:
        return abs(self.process_expr(obj[1]))

    def process_gimmeh(self, var):
        var_name = var[1]
        # check that variable exists
        self.get_var(var_name)

        self.vars[var_name] = input()

    def process_assign(self, args):
        var_name = args[0][1]
        value = self.process_expr(args[1][1])
        # check that variable exists
        self.get_var(var_name)

        self.vars[var_name] = value

    def process_decl(self, args):
        var_name = args[0][1]
        value = None if args[1] is None else self.process_value(args[1][1])

        self.vars[var_name] = value

    def process_cast(self, args):
        var_name = args[0][1]
        t = args[1]
        # check that variable exists
        self.get_var(var_name)

        self.vars[var_name] = self.totype(t, self.vars[var_name])

    def process_if_else(self, args):
        if_true, if_elses, if_false = args
        processed = False

        if self.it:
            self.process_statements(if_true)
            processed = True
        else:
            if if_elses is not None:
                for expr, statements in if_elses:
                    if self.process_expr(expr[1]):
                        processed = True
                        self.process_statements(statements)
                        break

        if not processed:
            if if_false is not None:
                self.process_statements(if_false)

    def process_loop(self, args):
        old_vars = dict(self.vars)
        local_var_name = args[0][1]
        self.vars[local_var_name] = 0

        if args[1] == UPPIN:
            f = lambda x: x + 1
        else:
            f = lambda x: x - 1

        loop_type = args[2][0]
        cond = args[2][1][1]
        statements = args[3]

        if loop_type == TIL:
            stop = lambda x: x
        else:
            stop = lambda x: not x

        while not stop(self.process_expr(cond)):
            self.process_statements(statements)
            self.vars[local_var_name] = f(self.vars[local_var_name])

        self.vars = old_vars

    def run(self, code):
      try:
        self.interpret(parse(code))
      except Exception as e:
        print("An error occured:")
        print(e)