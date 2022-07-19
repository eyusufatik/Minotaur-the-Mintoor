import os
from helpers import *

def clear_on_entry(func):
    def f(*args, **kwargs):
        os.system('cls' if os.name == 'nt' else 'clear')
        return func(*args, **kwargs)
    return f

def add_margin(func):
    def f(*args, **kwargs):
        my_print("")
        return func(*args, **kwargs)
    return f