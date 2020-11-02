import unittest
import sys

sys.path.append('/scripts/')
from common import remove_comments_from_code, count_keywords


class TestCountKeywords(unittest.TestCase):

    code_str = '"""For this is a comment to print"""\ndef test():\n    # for test\n    print("for")\n    a="""for"""\nb="for print"'

    code_str_2 = "'''For this is a comment to print'''\ndef test():\n    # for test\n    print('for')\n    a='''for'''\nb='for print'"

    def test_remove_comments_from_code(self) -> None:
        for s in [TestCountKeywords.code_str, TestCountKeywords.code_str_2]:
            print(s)
            
            p_code_str = remove_comments_from_code(s)
            
            print(p_code_str)
            
            self.assertTrue('#' not in p_code_str)
            self.assertTrue('"""' not in p_code_str)
        
    def test_count_keywords(self) -> None:
        for s in [TestCountKeywords.code_str, TestCountKeywords.code_str_2]:
            keyword_count = count_keywords(s)
            expected_count = (0, 0, 0, 0, 0, 0, 0, 1, 0, 1)
            
            print(keyword_count)
            
            for keyword, expected in zip(keyword_count, expected_count):
                self.assertTrue(keyword == expected, f'{expected} != {keyword}')

if __name__ == '__main__':
    tester = TestCountKeywords()

    tester.test_remove_comments_from_code()
    tester.test_count_keywords()
