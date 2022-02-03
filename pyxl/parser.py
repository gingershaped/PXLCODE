from ply import *
import pyxl.lexer as lexer
from .constants import *
from .errors import *

tokens = lexer.tokens


def p_program(p):
    '''program : HAI FLOAT NEWLINE statements KTHXBYE'''
    p[0] = p[4] if p[4] else []


def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 2:
        p[0] = []
        if p[1]:
            p[0].append(p[1])
    else:
        p[0] = p[1] if p[1] else []

        if p[2]:
            p[0].append(p[2])


def p_statement(p):
    '''statement : command NEWLINE
                 | command COMMA'''
    p[0] = p[1]


def p_command(p):
    '''command : empty
               | expr
               | call
               | cast
               | decl
               | assign_bukkit
               | assign
               | if_else
               | function
               | loop'''
    p[0] = p[1]


def p_command_loop(p):
    '''loop : IM IN YR variable operation YR variable condition expr NEWLINE statements IM OUTTA YR variable'''
    p[0] = (LOOP, (p[7], p[5], (p[8], p[9]), p[11]))


def p_operation(p):
    '''operation : UPPIN
                 | NERFIN'''
    p[0] = p[1]


def p_condition(p):
    '''condition : TIL
                 | WILE'''
    p[0] = p[1]


def p_command_if_else(p):
    '''if_else : O RLY QUESTION NEWLINE YA RLY NEWLINE statements NO WAI NEWLINE statements OIC'''
    p[0] = (IF_ELSE, [p[8], None, p[12]])


def p_command_if_else_short(p):
    '''if_else : O RLY QUESTION NEWLINE YA RLY NEWLINE statements OIC'''
    p[0] = (IF_ELSE, [p[8], None, None])


def p_command_if_else_extended(p):
    '''if_else : O RLY QUESTION NEWLINE YA RLY NEWLINE statements elifs NO WAI NEWLINE statements OIC'''
    p[0] = (IF_ELSE, [p[8], p[9], p[13]])


def p_command_elifs(p):
    '''elifs : elifs elif
             | elif'''
    if len(p) == 2:
        p[0] = []
        if p[1]:
            p[0].append(p[1])
    else:
        p[0] = p[1] if p[1] else []

        if p[2]:
            p[0].append(p[2])


def p_command_elif(p):
    '''elif : MEBBE expr NEWLINE statements'''
    p[0] = (p[2], p[4])


def p_command_decl(p):
    '''decl : I HAS A variable
            | I HAS A variable ITZ expr
            | I HAS A variable ITZ A type'''
    if len(p) == 5:
        p[0] = (DECLARE, [p[4], None, False])
    elif len(p) == 7:
        p[0] = (DECLARE, [p[4], p[6], False])
    else:
      p[0] = (DECLARE, [p[4], p[7], True])

def p_command_assign_bukkit(p):
    '''assign_bukkit : variable HAS A variable ITZ expr'''
    p[0] = (ASSIGN_BUKKIT, [p[1], p[4], p[6]])
def p_command_assign(p):
    '''assign : variable R expr'''
    p[0] = (ASSIGN, [p[1], p[3]])

def p_expr_get_bukkit(p):
    '''expr : variable APOSTROPHE_Z variable'''
    p[0] = (EXPR, (GET_BUKKIT, [p[1], p[3]]))


def p_command_cast(p):
    '''cast : variable IS NOW A type
            | variable R MAEK variable A type
            | variable R MAEK variable type'''
    if p[2] == 'IS':
        p[0] = (CAST, [p[1], p[5]])
    elif len(p) == 7:
        p[0] = (CAST, [p[1], p[6]])
    else:
        p[0] = (CAST, [p[1], p[5]])


def p_args(p):
    '''args : args expr
            | expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] if p[1] else []

        if p[2]:
            p[0].append(p[2])


def p_sep_args(p):
    '''sep_args : sep_args AN expr
            | expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] if p[1] else []

        if p[3]:
            p[0].append(p[3])

def p_sep_yr_args(p):
    '''sep_yr_args : sep_yr_args AN YR expr
            | expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] if p[1] else []

        if p[4]:
            p[0].append(p[4])

def p_command_function(p):
    '''function : HOW IZ I ID YR sep_yr_args NEWLINE statements IF U SAY SO'''
    p[0] = (FUNCTION, [p[4], p[6], p[8]])
def p_command_function_no_args(p):
    '''function : HOW IZ I ID NEWLINE statements IF U SAY SO'''
    p[0] = (FUNCTION, [p[4], p[6], []])

def p_expr_call_function(p):
    '''expr : I IZ ID YR sep_yr_args MKAY'''
    p[0] = (FUNCTION_CALL, [p[3], p[5]])
def p_expr_call_function_no_args(p):
    '''expr : I IZ ID'''
    p[0] = (FUNCTION_CALL, [p[3], []])

def p_type(p):
    '''type : YARN
            | NUMBR
            | NUMBAR
            | NOOB
            | BUKKIT'''
    p[0] = p[1]


def p_value_string(p):
    '''value : STRING'''
    p[0] = (VALUE, (YARN, p[1][1:-1]))


def p_value_float(p):
    '''value : FLOAT'''
    p[0] = (VALUE, (NUMBAR, p[1]))


def p_value_int(p):
    '''value : INTEGER'''
    p[0] = (VALUE, (NUMBR, p[1]))


def p_value_bool(p):
    '''value : WIN
             | FAIL'''
    p[0] = (VALUE, (TROOF, p[1]))

def p_value_dict(p):
  '''value : DICT'''
  p[0] = (VALUE, (BUKKIT, p[1]))


def p_call_visible_newline(p):
    '''call : VISIBLE args
            | VISIBLE args EXCLAMATION'''
    newline = len(p) == 3
    p[0] = (VISIBLE, (p[2], newline))


def p_call_gimmeh(p):
    '''call : GIMMEH variable'''
    p[0] = (GIMMEH, p[2])

def p_expr_unary(p):
  '''expr : SIZE OF expr
          | ABSLUT OF expr'''
  if p[1] == "SIZE":
    op = SIZE
  elif p[1] == "ABSLUT":
    op = ABSLUT
  else:
    print('UNKNOW UNARY OPERATOR', p[1])
    p.parser.error = 1
    return
  p[0] = (EXPR, (op, p[3]))

def p_expr_value(p):
    '''expr : value'''
    p[0] = (EXPR, p[1])


def p_expr_var(p):
    '''expr : variable'''
    p[0] = (EXPR, p[1])


def p_expr_math(p):
    '''expr : SUM OF expr AN expr
            | DIFF OF expr AN expr
            | PRODUKT OF expr AN expr
            | QUOSHUNT OF expr AN expr
            | MOD OF expr AN expr
            | BIGGR OF expr AN expr
            | SMALLR OF expr AN expr'''
    if p[1] == 'SUM':
        op = SUM
    elif p[1] == 'DIFF':
        op = DIFF
    elif p[1] == 'PRODUKT':
        op = PRODUKT
    elif p[1] == 'QUOSHUNT':
        op = QUOSHUNT
    elif p[1] == 'MOD':
        op = MOD
    elif p[1] == 'BIGGR':
        op = BIGGR
    elif p[1] == 'SMALLR':
        op = SMALLR
    else:
        print('unknown math operator', p[1])
        p.parser.error = 1
        return

    p[0] = (EXPR, (op, [p[3], p[5]]))


def p_expr_logic(p):
    '''expr : BOTH OF expr AN expr
            | EITHER OF expr AN expr
            | WON OF expr AN expr
            | NOT expr
            | ALL OF sep_args MKAY
            | ANY OF sep_args MKAY
            | ALL OF args MKAY
            | ANY OF args MKAY'''
    if p[1] == 'BOTH':
        op = BOTH
        p[0] = (EXPR, (op, [p[3], p[5]]))
    elif p[1] == 'EITHER':
        op = EITHER
        p[0] = (EXPR, (op, [p[3], p[5]]))
    elif p[1] == 'WON':
        op = WON
        p[0] = (EXPR, (op, [p[3], p[5]]))
    elif p[1] == 'NOT':
        op = NOT
        p[0] = (EXPR, (op, p[2]))
    elif p[1] == 'ALL':
        op = ALL
        p[0] = (EXPR, (op, p[3]))
    elif p[1] == 'ANY':
        op = ANY
        p[0] = (EXPR, (op, p[3]))
    else:
        print('unknown logic operator', p[1])
        p.parser.error = 1
        return


def p_expr_comp(p):
    '''expr : BOTH SAEM expr AN expr
            | DIFFRINT expr AN expr'''
    if p[1] == 'BOTH':
        p[0] = (EXPR, (SAME, [p[3], p[5]]))
    else:
        p[0] = (EXPR, (DIFFRINT, [p[2], p[4]]))


def p_expr_concat(p):
    '''expr : SMOOSH sep_args MKAY
            | SMOOSH args MKAY'''
    p[0] = (EXPR, (SMOOSH, p[2]))


def p_expr_cast(p):
    '''expr : MAEK expr A type
            | MAEK expr type'''
    if len(p) == 5:
        p[0] = (EXPR, (MAEK, [p[2], p[4]]))
    else:
        p[0] = (EXPR, (MAEK, [p[2], p[3]]))


def p_variable(p):
    '''variable : ID
                | IT'''
    p[0] = (VAR, p[1])

def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1
    raise UnexpectedTokenError(p[1])


# Empty
def p_empty(p):
    '''empty : '''


# Catastrophic error handler
def p_error(p):
    if not p:
        print("O NOES! SUMTHIN'S GON HORIBLY WRONG. DID U MAEK A TYPO?")


bparser = yacc.yacc()


def parse(data):
    bparser.error = 0
    p = bparser.parse(data)
    if bparser.error: return None
    return p
