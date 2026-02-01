from os.path import abspath, dirname


def get_path(relative_path: str, filename: str) -> str:
    """
    返回relative_path所在目录的filename地址
    :param relative_path:
    :param filename:
    :return: str
    """
    return f"{dirname(abspath(relative_path))}\\{filename}"
