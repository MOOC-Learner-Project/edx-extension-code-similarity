import sqlite3
import random
import os
import ast
import numpy as np

from typing import Dict
from scipy import mean
from numpy import nan
from pyflakes import checker, messages

from common import *


NEGATIVE_PROBABILITY = 0.2
POSITIVE = "positive"
NEGATIVE = "negative"
NOT = "not"
NOT_THRESHOLD = 3
SOMEWHAT = "somewhat"
SOMEWHAT_THRESHOLD = 2
MOSTLY = "mostly"
MOSTLY_THRESHOLD = 1
VERY = "very"
VERY_THRESHOLD = 0
UNDEFINED_ERRORS_TO_IGNORE = {'1-1': ['s'], '1-2': ['s'], '1-3': ['s']}
ERROR_TYPES_TO_IGNORE = (
    messages.UnusedImport,
    messages.RedefinedInListComp,
    messages.RedefinedWhileUnused,
    messages.ImportShadowedByLoopVar,
    messages.ImportStarNotPermitted,
    messages.ImportStarUsed,
    messages.ImportStarUsage,
    messages.MultiValueRepeatedKeyLiteral,
    messages.MultiValueRepeatedKeyVariable,
    messages.LateFutureImport,
    messages.UnusedVariable,
    messages.IsLiteral
)
UNDEFINED_ERRORS = (
    messages.UndefinedName,
    messages.UndefinedExport,
    messages.UndefinedLocal,
    messages.FutureFeatureNotDefined
)

def validate(code: str, pb: str) -> bool:
    try:
        tree = ast.parse(code)
        results = checker.Checker(tree)

        for error in results.messages:
            if isinstance(error, UNDEFINED_ERRORS):
                for arg in error.message_args:
                    if arg not in UNDEFINED_ERRORS_TO_IGNORE[pb]:
                        return False
            elif not isinstance(error, ERROR_TYPES_TO_IGNORE):
                return False
        return True
    except SyntaxError:
        return False


def get_similarity_string(delta: int) -> str:
    if delta >= NOT_THRESHOLD:
        return NOT
    elif delta >= SOMEWHAT_THRESHOLD:
        return SOMEWHAT
    elif delta >= MOSTLY_THRESHOLD:
        return MOSTLY
    elif delta >= VERY_THRESHOLD:
        return VERY


def get_subjective_string(delta: int, sentiment: str = POSITIVE) -> str:
    feedback: Dict[str, Dict[str, str]] = {
        NOT: {
            POSITIVE: "You can figure it out if you just keep trying!",
            NEGATIVE: "Try harder and you will figure it out.",
        },
        SOMEWHAT: {
            POSITIVE: "That is a good start! Keep putting in effort and you will figure it out!",
            NEGATIVE: "You have made some progress, but you need to put more effort in to succeed.",
        },
        MOSTLY: {
            POSITIVE: "Your efforts are showing! If you keep putting in effort you will succeed in no time!",
            NEGATIVE: "You have made some progress, but you need to put more effort in to succeed.",
        },
        VERY: {POSITIVE: "Amazing job! Your hard work paid off!"},
    }

    if delta >= NOT_THRESHOLD:
        return feedback[NOT][sentiment]
    elif delta >= SOMEWHAT_THRESHOLD:
        return feedback[SOMEWHAT][sentiment]
    elif delta >= MOSTLY_THRESHOLD:
        return feedback[MOSTLY][sentiment]
    elif delta >= VERY_THRESHOLD:
        return feedback[VERY][POSITIVE]


def get_closest_count(user_counts, previous_counts):
    min_dist = float('inf')
    min_count = None
    
    for previous in set(previous_counts):
        dist = n_dimension_dist(user_counts, previous)
        if dist < min_dist:
            min_dist = dist
            min_count = previous

    return min_count


def get_similarity(code: str, pb: str, subjective: bool = False,
                   should_validate: bool = True, storage: str = STORAGE) -> str:
    if should_validate and not validate(code, pb):
        return "The code submitted is invalid. Please fix it."

    db_cursor = sqlite3.connect(os.path.join(storage, pb, COUNTS_DB)).cursor()
    db_cursor.execute("SELECT * FROM counts")
    previous_counts = db_cursor.fetchall()

    user_counts = count_keywords(code)
    closest_count = get_closest_count(user_counts, previous_counts)

    delta_per_keyword = np.absolute(np.array(user_counts) - np.array(closest_count))
    delta = sum(delta_per_keyword) + delta_per_keyword[KEYWORDS.index('for')] \
                                   + delta_per_keyword[KEYWORDS.index('while')]
    
    sim_str = get_similarity_string(delta)
    response = f"Your code is {sim_str} similar to correct solutions submitted by other students in previous years."

    if subjective:
        sentiment = POSITIVE if random.random() > NEGATIVE_PROBABILITY else NEGATIVE
        feedback = get_subjective_string(percent, sentiment)
        response = f"{response}\n{feedback}"

    return response

if __name__ == "__main__":
    print(get_similarity('for print if', '1-1', should_validate=False))
