from .parser import parse
from .constants import *
import traceback, sys

class Interpreter(object):
    def __int__(self, ast):
        self.reset()

    def reset(self):
        self.vars = {}
        self.funcs = {}
        self.it = None
        self.interpreter = self
        self.exports = {}

    def interpret(self, ast):
        self.reset()
        self.process_statements(ast)

    def process_statements(self, statements, context=None):
        if not context:
            context = self
        if not len(statements):
          raise Exception("LOSE WHILE PARSE PROGRAM. MAEK SHUR U TYPE \"HAI\" AN \"KTHXBYE\" CORREKT.")
        for statement in statements:
            try:
                node_type, value = statement
                if node_type == EXPR:
                    self.process_expr(value, context)
                if node_type == VISIBLE:
                    self.process_visible(value, context)
                if node_type == GIMMEH:
                    self.process_gimmeh(value, context)
                if node_type == ASSIGN:
                    self.process_assign(value, context)
                if node_type == ASSIGN_BUKKIT:
                  self.process_assign_bukkit(value, context)
                if node_type == DECLARE:
                    self.process_decl(value, context)
                if node_type == DECLARE_BUKKIT_BLOCK:
                    self.process_decl_bukkit_block(value, context)
                if node_type == DECLARE_BUKKIT:
                  self.process_decl_bukkit(value, context)
                if node_type == CAST:
                    self.process_cast(value, context)
                if node_type == IF_ELSE:
                    self.process_if_else(value, context)
                if node_type == LOOP:
                    self.process_loop(value, context)
                if node_type == FUNCTION:
                    self.process_function(value, context)
                if node_type == FUNCTION_RETURN:
                    return self.process_return(value, context)
                if node_type == EXPORT:
                    self.process_export(value, context)
                if node_type == IMPORT:
                    self.process_import(value, context)
            except Exception as e:
                print("O NOES! AN EROR OCCURD:")
                print(e)
                self.lastError = sys.exc_info()
                print("in instruction:")
                print(statement)
                self.lastError = sys.exc_info()
                return

    def expr_res(self, res):
        self.it = res
        return res

    def process_expr(self, expr, context):
        node_type, value = expr
        if node_type == FUNCTION_CALL:
            return self.execute_function(value, context)
        if node_type == VALUE:
            return self.expr_res(self.process_value(value))
        if node_type == VAR:
            return self.expr_res(self.process_variable(value, context))
        if node_type == GET_BUKKIT:
           return self.process_get_bukkit(value, context)
        if node_type in [SIZE, ABSLUT]:
          return self.expr_res(self.process_unary(node_type, value))
        if node_type in [SUM, DIFF, PRODUKT, QUOSHUNT, MOD, BIGGR, SMALLR]:
            return self.expr_res(self.process_math_expr(node_type, value, context))
        if node_type in [BOTH, EITHER, WON, NOT, ALL, ANY]:
            return self.expr_res(self.process_logic_expr(node_type, value, context))
        if node_type in [SAME, DIFFRINT]:
            return self.expr_res(self.process_equality(node_type, value, context))
        if node_type == SMOOSH:
            return self.expr_res(self.process_smoosh(value, context))
        if node_type == MAEK:
            return self.expr_res(self.process_expr_cast(value, context))

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
                raise Exception('DONT KNO VARIABLE FOR TROOF TYP')
        if node_type == BUKKIT:
          return {}

    def get_var(self, var_name, context):
        if var_name in context.vars:
            return context.vars[var_name]

        raise Exception('VARIABLE {}: USED BFOR DECLARATIN'.format(var_name))

    def process_variable(self, var_name, context):
        if var_name == 'IT':
            return self.it

        return self.get_var(var_name, context)

    def process_math_expr(self, op, args, context):
        lhs = self.process_expr(args[0][1], context)
        rhs = self.process_expr(args[1][1], context)

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

    def process_logic_expr(self, op, args, context):
        if op in [BOTH, EITHER, WON]:
            lhs = self.process_expr(args[0][1], context)
            rhs = self.process_expr(args[1][1], context)

            if op == BOTH:
                return lhs and rhs
            if op == EITHER:
                return lhs or rhs
            if op == WON:
                return bool(lhs) ^ bool(rhs)
        if op == NOT:
            lhs = self.process_expr(args[1], context)
            return not lhs
        if op == ALL or op == ANY:
            exprs = [self.process_expr(arg[1], context) for arg in args]

            if op == ALL:
                return all(exprs)
            if op == ANY:
                return any(exprs)

    def process_equality(self, op, args, context):
        lhs = self.process_expr(args[0][1], context)
        rhs = self.process_expr(args[1][1], context)

        if op == SAME:
            return lhs == rhs
        if op == DIFFRINT:
            return lhs != rhs

    def process_smoosh(self, args, context):
        str_args = ''.join([str(self.process_expr(arg[1]), context) for arg in args])
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

    def process_visible(self, args, context):
        to_print, new_line = args
        to_print = ''.join([str(self.process_expr(arg[1], context)) for arg in to_print])

        print(to_print, end='\n' if new_line else '')

    def process_unary(self, expr, obj):
      if expr == SIZE:
        return len(self.process_expr(obj[1]))
      elif expr == ABSLUT:
        return abs(self.process_expr(obj[1]))

    def process_gimmeh(self, var, context):
        var_name = var[1]
        # check that variable exists
        context.get_var(var_name, context)

        context.vars[var_name] = input()

    def process_assign(self, args, context):
        var_name = args[0][1]
        value = self.process_expr(args[1][1], context)
        # check that variable exists
        context.get_var(var_name, context)

        context.vars[var_name] = value
    
    def process_assign_bukkit(self, args, context):
        self.get_var(args[0][1], context).vars[args[1][1]] = self.process_expr(args[2][1])

    def process_get_bukkit(self, args, context):
        return self.get_var(args[0][1], context).vars[args[1][1]]

    def process_decl(self, args, context):
        var_name = args[0][1]
        if args[2]:
          t = args[1]
          v = None
          if t == YARN:
            v = ""
          elif t == NUMBR:
            v = 0
          elif t == NUMBAR:
            v = 0.0
          elif t == TROOF:
            v = False
          elif t == BUKKIT:
            v = Bukkit(context.interpreter)
          else:
            raise Exception("INVALID TYP FOUR VARIABLE: " + t)
          context.vars[var_name] = v
        else:
          value = None if args[1] is None else self.process_expr(args[1][1], context)

          context.vars[var_name] = value

    def process_export(self, args, context):
        for arg in args:
            if arg[1][0] != "VARIABLE":
                raise Exception(str(arg[1]) + " CANNOT EXPORT THAT!")
            else:
                try:
                    v = self.get_var(arg[1][1], context)
                except:
                    v = self.funcs[arg[1][1]]
                self.exports[arg[1][1]] = v
    def process_import(self, path, context):
        path = path[1:-1]
        f = ""
        for p in ["."] + __path__:
            try:
                f = open(p + "/" + path + ".pxl").read()
            except FileNotFoundError:
                continue
            except Exception as e:
                raise ImportError("ERROR OCCURED WHILE IMPORTING " + path + ": " + str(e)) from None
            else:
                break
        if not f:
            raise ImportError("NO SUCH FILE: " + path + ".pxl") from None
        i = Interpreter()
        i.run(f)
        for o in i.exports:
            if isinstance(i.exports[o], Function):
                self.funcs[o] = i.exports[o]
            else:
                self.vars[o] = i.exports[o]

    def process_decl_bukkit_block(self, args, context):
        b = Bukkit(context)
        for statement in args[1]:
            node_type, value = statement
            if node_type == DECLARE:
                self.process_decl(value, b)
            elif node_type == FUNCTION:
                if value[0]:
                    raise Exception("CANNOT DECLARE OWNED VARIABLE INSIDE BUKKIT BLOCK")
                else:
                    self.process_function(value, b)
        context.vars[args[0][1]] = b
    def process_cast(self, args, context):
        var_name = args[0][1]
        t = args[1]
        # check that variable exists
        context.get_var(var_name)

        context.vars[var_name] = self.totype(t, context.vars[var_name])

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

    def process_function(self, args, context):
        if args[0]:
            context = context.get_var(args[0][1], context)
        context.funcs[args[1]] = Function(context, context.interpreter, args[2], args[3])
    def execute_function(self, args, context):
        if args[0]:
            context = context.interpreter.get_var(args[0][1], context)
        try:
            return context.funcs[args[1]].execute([self.process_expr(x[1], context) for x in args[2]])
        except KeyError:
            raise Exception("NO FUNCTION NAEMD " + args[1])
    def process_return(self, args, context):
        if args:
            return self.process_expr(args[1], context)
        else:
            return None

    def process_loop(self, args, context):
        local_var_name = args[0][1]
        context.vars[local_var_name] = 0

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

        while not stop(self.process_expr(cond, context)):
            self.process_statements(statements, context)
            context.vars[local_var_name] = f(context.vars[local_var_name])

        context.vars.pop(local_var_name)

    def run(self, code):
        self.interpret(parse(code))
        

class Bukkit():
    def __init__(self, interpreter):
        self.vars = {"ME": self}
        self.funcs = {}
        self.interpreter = interpreter

class Function():
    def __init__(self, parent, interpreter, instructions, parameters):
        self.instructions = instructions
        self.vars = {"ME": parent}
        self.funcs = {}
        self.interpreter = interpreter
        self.parent = parent
        self.parameters = parameters
    def execute(self, parameters):
        if len(parameters) != len(self.parameters):
            raise Exception("WRONG NUMBR OF PARAMETUHS: GOT " + str(len(parameters)) + " BUT EXPECTED " + str(len(self.parameters)))
        for c, p in enumerate(self.parameters):
            self.vars[p[1][1]] = parameters[c]
        return self.interpreter.process_statements(self.instructions, self)
    def get_var(self, var_name, context):
        if var_name in context.vars:
            return context.vars[var_name]

        raise Exception('variable {}: used before declaration'.format(var_name))