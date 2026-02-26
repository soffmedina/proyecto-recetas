from colorama import init, Fore, Style
import sys

# init de colorama para los colores en terminal
init(autoreset=True)

# algunas consolas (especialmente Windows con cp1252) no pueden imprimir
# caracteres emoji; si tratamos de hacerlo se lanza UnicodeEncodeError. Para
# evitar que cada print falle, verificamos si el stdout actual admite el
# carácter y, en caso contrario, lo reemplazamos por cadena vacía.

def _safe_emoji(char: str) -> str:
    try:
        if sys.stdout and sys.stdout.encoding:
            char.encode(sys.stdout.encoding)
        return char
    except Exception:
        return ""

def info(msg):
    return Fore.CYAN + _safe_emoji("ℹ️") + msg

def success(mgs):
    return Fore.GREEN + _safe_emoji("✅") + mgs

def warn(msg):
    return Fore.YELLOW + _safe_emoji("⚠️") + msg

def error(msg):
    return Fore.RED + _safe_emoji("❌") + msg

def title(msg):
    return Style.BRIGHT + msg

