import re
from web3 import Web3
from colorama import Fore, Style, init, Back, ansi

init(False)
print(Back.BLACK)
print(ansi.clear_screen())

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_number_selection(end: int, number: int):
    return number in range(end + 1)


def get_int_answer():
    inp = None
    try:
        inp = input("> ")
        answer = int(inp)
        return True, answer
    except Exception:
        return False, inp


def my_print(msg: str, *args, **kwargs):
    print(f"{Back.BLACK}{Fore.GREEN}{msg}", *args, **kwargs)


def end_style():
    print(Style.RESET_ALL)


def is_valid_url(url: str):
    global regex
    return re.match(regex, url) is not None


def create_web3_instance(url: str):
    return Web3(Web3.HTTPProvider(url))
