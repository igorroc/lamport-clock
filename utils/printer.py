from colorama import Fore, Style

def config(string):
    print(f"{Fore.RED}[CONFIG]{Style.RESET_ALL} {string}")

def error(string):
    print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} {string}")

def warning(string):
    print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {string}")

def info(string):
    print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {string}")

def success(string):
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {string}")
