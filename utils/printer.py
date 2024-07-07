from colorama import Fore, Style

def config(count, string):
    print(f"{Fore.RED}[CONFIG {count:03d}]{Style.RESET_ALL} {string}")

def error(count, string):
    print(f"{Fore.RED}[ERRO {count:03d}]{Style.RESET_ALL} {string}")

def warning(count, string):
    print(f"{Fore.YELLOW}[WARN {count:03d}]{Style.RESET_ALL} {string}")

def info(count, string):
    print(f"{Fore.BLUE}[INFO {count:03d}]{Style.RESET_ALL} {string}")

def success(count, string):
    print(f"{Fore.GREEN}[SUCESSO {count:03d}]{Style.RESET_ALL} {string}")
