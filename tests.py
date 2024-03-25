import unittest
from aws_json import verify_json_input

class TestStringMethods(unittest.TestCase):
    def test_resource_with_asterisk(self):
        self.assertEqual(verify_json_input("tests/resource_with_asterisk/json_example.json"), False)

    def test_invalid_json_format(self):
        self.assertEqual(verify_json_input("tests/invalid_json_format/invalid1.json"), True)

    

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()