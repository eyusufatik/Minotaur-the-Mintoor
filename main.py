import os
from helpers import end_style
from prompts import *
from account_manager import AccountManager

# Unnecessary ascii art
ansi_lines = open("ascii-art.ans").readlines()
ansi_str = "".join(ansi_lines)
my_print(ansi_str,end="")

try:
    main_prompt()
except KeyboardInterrupt:
    end_style()
    os.system('cls' if os.name == 'nt' else 'clear')