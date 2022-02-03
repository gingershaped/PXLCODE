class UnexpectedTokenError(Exception):
  def __init__(self,  token):
    self.token = token
  def __str__(self):
    return "O NOES! AN ERROR HAZ OCCURD WHILE PARSING: UNEXPEKTED TOKEN: " + str(self.token.value) + " (" + self.token.type + ") AT LINE " + str(self.token.lineno) + " (CHAR " + str(self.token.lexpos) + ")"