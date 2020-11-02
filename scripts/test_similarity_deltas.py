import unittest
import numpy as np
from collections import Counter, defaultdict        

from compare_trajectories import *
from store_counts import store_counts

TEST_OUTPUT = 'test_output'

SIMILARITY_ORDER = [NOT, SOMEWHAT, MOSTLY, VERY]

DELTA_THRESHOLD = 10

class TestCompareTrajectories(unittest.TestCase):
    golden_keywords = {
        '1-1': 'for if print',
        '1-2': 'for if print'
    }

    def similarity_deltas_multiple_thresholds(self) -> None:
        thresholds = [i/DELTA_THRESHOLD for i in range(DELTA_THRESHOLD)]

        for threshold in thresholds:
            if not os.path.exists(TEST_OUTPUT):
                os.mkdir(TEST_OUTPUT)

            storage = os.path.join(TEST_OUTPUT, str(threshold))
            store_counts(storage=storage, threshold=threshold)

            for pb, keywords in TestCompareTrajectories.golden_keywords.items():
                print(pb)
                counts = count_keywords(keywords)
                sim_strs = []
                for i in range(len(counts)):
                    test_count = list(counts)
                    if counts[i] >= 1:
                        test_count[i] -= 1
                        sim_strs.append(get_similarity_string(get_similarity_percent(test_count, pb, storage=storage)))
                        test_count[i] += 2
                    else:
                        test_count[i] += 1

                    sim_strs.append(get_similarity_string(get_similarity_percent(test_count, pb, storage=storage)))
                counts = Counter(sim_strs)
                    
                output_path = os.path.join(storage, f'golden_deltas_{pb}.txt')
                if os.path.exists(output_path):
                    open(output_path, 'w').close()
                
                with open(output_path, 'a') as f:
                    f.write('keyword, count\n')
                    for similarity_keyword in SIMILARITY_ORDER:
                        f.write(similarity_keyword + ", ")
                        try:
                            count = counts[similarity_keyword]
                        except KeyError:
                            count = 0
                        print(f"  {similarity_keyword}: {count}")
                        f.write(str(count) + '\n')

    def similarity_deltas_multiple_parameters(self) -> None:
        if not os.path.exists(TEST_OUTPUT):
            os.mkdir(TEST_OUTPUT)

        thresholds = np.arange(0.0, 1.0, 0.05)
        scales = np.arange(0.5, 1.5, 0.05)
        for threshold in thresholds:
            for scale in scales:
                store_counts(storage=TEST_OUTPUT, threshold=threshold, std_scale=scale)
                for pb, keywords in TestCompareTrajectories.golden_keywords.items():
                    counts = count_keywords(keywords)
                    sim_counts = {}

                    for n in range(1, 10):
                        all_test_counts = []

                        for i in range(len(counts)):
                            test_counts = list(counts)
                            test_counts[i] += n
                            all_test_counts.append(test_counts)

                            if counts[i] >= n:
                                test_counts[i] -= n*2
                                all_test_counts.append(test_counts)

                        for z in range(1, n):
                            for i in range(len(counts) - 1):
                                test_counts = list(counts)
                                test_counts[i] += n-z
                                test_counts[i+1] += z
                                all_test_counts.append(test_counts)

                                if counts[i] >= n-z and counts[i+1] >= z:
                                    test_counts[i] -= (n-z)*2
                                    test_counts[i+1] -= z*2
                                    all_test_counts.append(test_counts)

                            for k in range(1, z):
                                for i in range(len(counts) - 2):
                                    test_counts = list(counts)
                                    test_counts[i] += n-z-k
                                    test_counts[i+1] += z-k
                                    test_counts[i+2] += k
                                    all_test_counts.append(test_counts)

                                    if counts[i] >= n-z-k and counts[i+1] >= z-k and test_counts[i+2] >= k:
                                        test_counts[i] -= (n-z-k)*2
                                        test_counts[i+1] -= (z-k)*2
                                        test_counts[i+2] -= k*2
                                        all_test_counts.append(test_counts)

                        unique_test_counts = [list(x) for x in set(tuple(x) for x in all_test_counts)]
                        sim_strs = [get_similarity_string(get_similarity_percent(c, pb, storage=TEST_OUTPUT)) for c in unique_test_counts]
                        current_counts = dict(Counter(sim_strs)) 

                        if n == 1 and 'very' not in current_counts:
                            break
                        elif n == 3 and len(current_counts) != 1:
                            break

                        sim_counts[n] = current_counts

                    if sim_counts:
                        print(pb, threshold, scale)
                        print("    " + str(sim_counts) + '\n')

    def similarity_deltas(self, threshold: float = 0.0, scale: float = 1.0) -> None:
        store_counts(storage=TEST_OUTPUT, threshold=threshold, std_scale=scale)
        for pb, keywords in TestCompareTrajectories.golden_keywords.items():
            counts = count_keywords(keywords)
            sim_counts = {}

            for n in range(1, 10):
                all_test_counts = []
                
                for i in range(len(counts)):
                    test_counts = list(counts)
                    test_counts[i] += n
                    all_test_counts.append(test_counts)

                    if counts[i] >= n:
                        test_counts[i] -= n*2
                        all_test_counts.append(test_counts)

                for z in range(1, n):
                    for i in range(len(counts) - 1):
                        test_counts = list(counts)
                        test_counts[i] += n-z
                        test_counts[i+1] += z
                        all_test_counts.append(test_counts)
                        
                        if counts[i] >= n-z and counts[i+1] >= z:
                            test_counts[i] -= (n-z)*2
                            test_counts[i+1] -= z*2
                            all_test_counts.append(test_counts)

                    for k in range(1, z):
                        for i in range(len(counts) - 2):
                            test_counts = list(counts)
                            test_counts[i] += n-z-k
                            test_counts[i+1] += z-k
                            test_counts[i+2] += k
                            all_test_counts.append(test_counts)
                            
                            if counts[i] >= n-z-k and counts[i+1] >= z-k and test_counts[i+2] >= k:
                                test_counts[i] -= (n-z-k)*2
                                test_counts[i+1] -= (z-k)*2
                                test_counts[i+2] -= k*2
                                all_test_counts.append(test_counts)

                unique_test_counts = [list(x) for x in set(tuple(x) for x in all_test_counts)]
                sim_strs = [get_similarity_string(get_similarity_percent(c, pb, storage=TEST_OUTPUT)) for c in unique_test_counts]
                current_counts = dict(Counter(sim_strs))

                sim_counts[n] = current_counts

            print(pb, sim_counts)

if __name__ == '__main__':
    tester = TestCompareTrajectories()
    tester.similarity_deltas_multiple_parameters()
    tester.similarity_deltas(threshold=0.7, scale=0.05)
