from compare_trajectories import get_similarity

def test_samples():
    print("1-1")
    print(get_similarity('for print if', '1-1', should_validate=False))
    print(get_similarity('for print if if if for', '1-1', should_validate=False))
    print(get_similarity('for print if if if if if', '1-1', should_validate=False))
    print(get_similarity('for', '1-1', should_validate=False))
    print(get_similarity('for print', '1-1', should_validate=False))
    print(get_similarity('for print if if if', '1-1', should_validate=False))
    print(get_similarity('a\na\np\na\nfor i in range(10):\n    print(i)\nr=2', '1-1'))

    print("1-2")
    print(get_similarity('for print if', '1-2', should_validate=False))
    print(get_similarity('for print', '1-2', should_validate=False))
    print(get_similarity('for break continue if print', '1-2', should_validate=False))

    print("1-3")
    print(get_similarity('for print if if else', '1-3', should_validate=False))
    print(get_similarity('for', '1-3', should_validate=False))
    print(get_similarity('for print', '1-3', should_validate=False))
    print(get_similarity('for print for if else if', '1-3', should_validate=False))
    

if __name__ == "__main__":
    test_samples()
