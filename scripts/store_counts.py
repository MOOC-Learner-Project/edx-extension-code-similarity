import os
import sys
import glob
import sqlite3
import numpy as np

from scipy.stats import pearsonr
from common import *
from extract_csv_data import extract_user_data, extract_golden_data

THRESHOLD = 0.5

def filter_data(data: list, golden: str, threshold: float) -> list:
    filtered = []

    golden_counts = count_keywords(golden)
    
    for solution in data:
        counts = count_keywords(solution)

        if any(counts) and pearsonr(golden_counts, counts)[0] > threshold:
            filtered.append(counts)

    cielings = np.quantile(np.array(filtered), 0.5, axis=0)
    k = 0
    while k < len(filtered):
        for i in range(len(filtered[k])):
            if filtered[k][i] > cielings[i]:
                del filtered[k]
                k -= 1
                break
        k += 1

    return filtered
            
def create_table(path: str, fname: str, values: list, table_name: str) -> None:
    n_vals = len(values[0])
    table_vals = ",".join([f"`{i}` integer NOT NULL" for i in range(n_vals)])        
    vals_str = ",".join(["?" for _ in range(n_vals)])
    db_conn = sqlite3.connect(os.path.join(path, fname))
    db_cursor = db_conn.cursor()
    db_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    db_cursor.execute(f"CREATE TABLE {table_name} ({table_vals})")
    db_cursor.executemany(f"INSERT INTO {table_name} VALUES ({vals_str})", values)
    db_conn.commit()

def store_counts(storage: str = STORAGE, threshold: float = THRESHOLD) -> None:
    if not os.path.isdir(storage):
        os.mkdir(storage)

    previous_solutions_by_problem = extract_user_data()
    golden_solutions = extract_golden_data()

    assert len(previous_solutions_by_problem) == len(golden_solutions)

    for pb in golden_solutions:
        golden_solution = golden_solutions[pb]
        previous_solutions = previous_solutions_by_problem[pb]
        counts = filter_data(previous_solutions, golden_solution, threshold)
        
        if counts:
            pb_path = os.path.join(storage, pb)
            if not os.path.isdir(pb_path):
                os.mkdir(pb_path)
                
            create_table(pb_path, COUNTS_DB, counts, COUNTS_DB_TABLE_NAME)

if __name__ == "__main__":
    store_counts()
