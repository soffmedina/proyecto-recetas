def format_title(title: str) -> str:
    """Capitaliza primera letra de cada palabra"""
    if not title:
        return ""
    return " ".join(word.capitalize() for word in title.split())


def clean_text(text: str) -> str:
    """Limpia espacios extra"""
    if not text:
        return ""
    return " ".join(text.split())