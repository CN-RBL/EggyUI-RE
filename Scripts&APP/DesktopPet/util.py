from os.path import abspath, dirname


def get_path(relative_path: str, filename: str) -> str:
    return f"{dirname(abspath(relative_path))}\\{filename}"
