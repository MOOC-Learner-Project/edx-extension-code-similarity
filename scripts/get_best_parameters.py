import itertools
import ast

import json

CHECKS = ['very', 'mostly', 'somewhat', 'not']

largest = {pb: [(0, 0, 0)]*len(CHECKS) for pb in ['1-1', '1-2', '1-3']}

lines = [line.rstrip('\n') for line in open('test.out')]
lines = [line for line in lines if line.strip()]

for i in range(0, len(lines)-1, 2):
    line1 = lines[i]
    line2 = lines[i+1]

    pb, threshold, scale = line1.split(' ')
    counts = ast.literal_eval(line2[4:])
    
    for n in range(len(CHECKS)):
        try:
            if counts[n+1][CHECKS[n]] > largest[pb][n][0]:
                largest[pb][n] = (counts[n+1][CHECKS[n]], threshold, scale, counts)
        except KeyError:
            pass


largest_overall = {pb: (0, 0, {1: {'very': 0}, 2: {'mostly': 0}, 3: {'somewhat': 0}, 4: {'not': 0}}) for pb in ['1-1', '1-2', '1-3']}
acceptable_delta = 0

for l_i in range(0, len(lines)-1, 2):
    line1 = lines[l_i]
    line2 = lines[l_i+1]

    pb, threshold, scale = line1.split(' ')
    counts = ast.literal_eval(line2[4:])

    if len(counts) < 4:
        continue
    better = True
    for i in range(1, 5):
        current = counts[i]
        current_val = current[CHECKS[i-1]]

        if current_val < largest_overall[pb][2][i][CHECKS[i-1]] - acceptable_delta or current_val < 2:
            better = False
            break

    if better:
        largest_overall[pb] = (threshold, scale, counts)

print(json.dumps(largest_overall, sort_keys=True, indent=4))