import os
import re
from typing import Tuple

KEYWORDS: Tuple[str, ...] = (
    "if",
    "elif",
    "else",
    "for",
    "while",
    "break",
    "continue",
    "def",
    "return",
    "print",
)

COUNTS_DB = "counts.sqlite3"
COUNTS_DB_TABLE_NAME = 'counts'
SCRIPTS = "/scripts/"
DATA = "/data/"


def add_data_to_path(path: str) -> str:
    return os.path.join(DATA, path)


STORAGE = add_data_to_path("STORAGE")


def remove_comments_from_code(code: str) -> str:
    """Removes comments and strings from code.
    
    :param code: input string to process
    :returns: The code without comments and strings.
    """
    code = re.sub(r"(#+)(.*)\n", "\n", code)  # single line comments
    code = re.sub(r"\"\"\"[\s\S]*?\"\"\"", "", code)  # multiline comments/strings

    # multiline comments/strings with apostrophe quotes
    code = re.sub(r'\'\'\'[\s\S]*?\'\'\'', "", code)

    # strings with single quotation marks
    code = re.sub(r"\"[\s\S]*?\"", "", code)

    # strings with single quotation marks with apostrophe quotes
    code = re.sub(r'\'[\s\S]*?\'', "", code)

    return code


def count_keywords(code: str) -> Tuple[int]:
    code = remove_comments_from_code(code)
    keyword_counts = []
    
    for keyword in KEYWORDS:
        keyword_counts.append(code.count(keyword))

    return tuple(keyword_counts)

def n_dimension_dist(a1: Tuple[int, ...], a2: Tuple[int, ...]) -> int:
    assert len(a1) == len(a2)
    
    sum_difference_squares = 0

    for i in range(len(a1)):
        sum_difference_squares += (a1[i] - a2[i])**2

    return sum_difference_squares**0.5
