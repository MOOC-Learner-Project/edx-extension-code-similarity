import glob
import ast
import re
import os
import collections
import pandas as pd

from common import add_data_to_path
from typing import Dict, Tuple, List
from pathlib import Path

GOLDEN_SOLUTIONS = add_data_to_path("golden_solutions")

def extract_user_data() -> Dict[Tuple[str, str], List[str]]:
    pb_solution_files = glob.glob(add_data_to_path("*.*"))

    correct_submissions = collections.defaultdict(list)
    
    for f in pb_solution_files:
        match = re.search(r'unit(\d+)_pb(\d+)', f)
        unit_problem = f"{match.group(1)}-{match.group(2)}"

        solutions = pd.read_csv(f)

        solutions = solutions[solutions.final_correct_bool]
        
        for ls in solutions.unique_correctness_list:
            assert bool(ast.literal_eval(ls)[0])
            
        for submissions in solutions.unique_submission_history:
            submission = ast.literal_eval(submissions)[0]
            
            correct_submissions[unit_problem].append(submission)

    return correct_submissions

def extract_golden_data() -> Dict[Tuple[str, str], List[str]]:
    golden_solution_files = Path(GOLDEN_SOLUTIONS).rglob("*.py")
    golden_solutions = {}

    for f in golden_solution_files:
        f = str(f)
        match = re.search(r'\d+-\d', f).group()

        golden_solutions[match] = open(f, 'r').read()

    return golden_solutions
        
if __name__ == '__main__':
    print(extract_user_data())
    print(extract_golden_data())
    
