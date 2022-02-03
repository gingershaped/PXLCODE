from pyxl import Interpreter
import traceback, sys, pprint, os.path

def run(code, interpreter, debug, autorestart):
  try:
    _ = interpreter.run(code)
    if autorestart:
      interpreter.reset()
  except (Exception) as e: print("\n".join(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))[:-1].lstrip(), file=sys.stderr)

def repl():
  print("PXLCODE REPL version 1.0")
  print("Made by GingerIndustries 2022")
  print("Type /help for help.")

  interpreter = Interpreter()
  autorestart = False
  outputnumbers = False
  pp = pprint.PrettyPrinter(indent=4)
  
  while True:
    try:
      code = input(">>> ")
    except KeyboardInterrupt:
      print("KTHXBYE!")
      exit()
    if code == "":
      pass
    elif code == "/help":
      print("""Commands list:
/help: Displays this menu
/load <path>: Loads and executes a .pol file
/loadabf <path>: Loads and executes an .abf file
/autorestart: Toggle auto-restart (the interpreter will restart every time a group of code is run, on by default)
/restart: Restart the interpreter
/memdump: Print the contents of memory
/toascii and /fromascii: Utilities that convert a number to ascii and a character from ascii.
      """)
    elif code == "/restart":
      print("==========INTERPRETER RESTART==========")
      interpreter.reset()
    elif code == "/memdump":
        print("Memory dump:")
        pp.pprint(interpreter.vars)
        print("Function dump:")
        pp.pprint([interpreter.funcs[x].vars for x in interpreter.funcs])
    elif code == "/autorestart":
      autorestart = not autorestart
      print("Autorestart", autorestart)
    elif code == "/traceback":
      try:
        traceback.print_exception(None, interpreter.lastError[1], interpreter.lastError[2])
      except TypeError:
        print("No traceback available")
    elif code == "/exit":
      exit(0)
    elif code.startswith("/load"):
      name = " ".join(code.split(" ")[1:])
      try:
        kc = open(name)
      except FileNotFoundError:
        print("O NOES! CANT FIND FILE:", name)
        continue
      except OSError as e:
        print("SUMTHIG WENT WRONG WHILE LODING FILE \"", name, "\":", str(e))
        continue
      interpreter.fileName = " ".join(code.split(" ")[1:])
      program = kc.read()
      kc.close()
      interpreter.reset()
      print("=====INTERPRETER RESTART=====")
      try:
        run(program, interpreter, False, False)
      except KeyboardInterrupt:
        print("Program terminated.")
      interpreter.fileName = "<shell>"
    elif code.startswith("/") and not code.startswith("/("):
      print("Invalid command")
    else:
      try:
        run(code, interpreter, False, autorestart)
      except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
  repl()