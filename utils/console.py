from colorama import init, Fore, Style

init(autoreset=True)     # ->Para iniciar colorama

def info(msg):
    return Fore.CYAN + "ℹ️" + msg

def success(mgs):
    return Fore.GREEN + "✅" + mgs

def warn(msg):
    return Fore.YELLOW + "⚠️" + msg

def error(msg):
    return Fore.RED + "❌" + msg

def title(msg):
    return Style.BRIGHT + msg

