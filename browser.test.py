# This, as any other file ending with ".test.*"
# is a test file! The code of that files should not
# be used in real-world scenarios. 


import webbrowser
from sys import exit

from constants import EXPECTED_PORT


OPEN_OR_CLOSE = input("What now (o/c)?  ").lower()

if OPEN_OR_CLOSE != "o":
  exit()

webbrowser.open(f"http://127.0.0.1:{EXPECTED_PORT}/test.html")
