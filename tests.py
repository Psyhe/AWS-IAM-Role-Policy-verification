import unittest
import json
import os

from aws_json import verify_json_input
from aws_json import verify_aws_json_format

import aws_json

class TestInvalidInput(unittest.TestCase):
    def test_invalid_json_format(self):
        self.assertEqual(verify_json_input("tests/invalid_json_format/invalid1.json"), True)
    
    def test_invalid_input_fromat(self):
        self.assertEqual(verify_json_input("tests/invalid_json_format/something.txt"), True)

class TestCorrectInput(unittest.TestCase):
    def test_resource_with_asterisk(self):
        self.assertEqual(verify_json_input("tests/valid_json/json_example.json"), False)

    def test_resource_without_asterisk_many_resources(self):
        self.assertEqual(verify_json_input("tests/valid_json/example_without_asterisk.json"), True)

    def test_resource_with_asterisk_many_resources(self):
        self.assertEqual(verify_json_input("tests/valid_json/json_multiple.json"), False)

class TestAbsolutePath(unittest.TestCase):
    def test_absolute_path(self):
        absolute_path = os.path.abspath("tests/valid_json/json_example.json")
        self.assertEqual(verify_json_input(absolute_path), False)

    def test_absolute_path2(self):
        absolute_path = os.path.abspath("tests/invalid_json_format/invalid1.json")
        self.assertEqual(verify_json_input(absolute_path), True)

class TestJsonString(unittest.TestCase):
    def test_wrong_policy_definition(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            },
            "PolicyAdditional": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_wrong_policy_name(self):
        json_string = """
        {
            "PolicyName": "root!",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_wrong_policy_document_format(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": "document"
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_lack_of_statement(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17"
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_additional_info_in_policy_document(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ],
                "Additional": "info"
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_asterisk_with_additional_characters(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*abc"
                    }
                ]
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_lack_of_statement(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Version": "2012-10-17"
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

    def test_lack_of_version(self):
        json_string = """
        {
            "PolicyName": "root",
            "PolicyDocument": {
                "Statement": [
                    {
                        "Sid": "IamListAccess",
                        "Effect": "Allow",
                        "Action": [
                            "iam:ListRoles",
                            "iam:ListUsers"
                        ],
                        "Resource": "*"
                    }
                ]
            }
        }
        """
        json_data = json.loads(json_string)
        self.assertEqual(verify_aws_json_format(json_data), True)

class TestPolicyName(unittest.TestCase):
    def test_too_long_policy_name(self):
        self.assertEqual(aws_json.verify_policy_name_properties("a" * 129), True)

    def test_wrong_policy_name(self):
        self.assertEqual(aws_json.verify_policy_name_properties("root!"), True)

    def test_wrong_policy_name2(self):
        self.assertEqual(aws_json.verify_policy_name_properties("root*"), True)

    def test_empty_policy_name(self):
        self.assertEqual(aws_json.verify_policy_name_properties(""), True)

    def test_json_name_format(self):
        self.assertEqual(aws_json.verify_policy_name_properties("{ Resource: '*',}"), True)

    def test_correct_policy_name(self):
        self.assertEqual(aws_json.verify_policy_name_properties("root"), False)

    def test_correct_policy_name2(self):
        self.assertEqual(aws_json.verify_policy_name_properties("ROOT123@"), False)

class TestStatement(unittest.TestCase):
    def test_not_list_format(self):
        self.assertEqual(aws_json.verify_list_of_statements({"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*"}), True)

    def test_acceptable_additional_fields(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*"}, {"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*"}]), False)

    # In case there occurs an additional field in the statement, the function should return True despite the "*" in the Resource field
    def test_unacceptable_additional_fields(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*"}, {"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*", "Additional": "info"}]), True)
    
    def test_additional_characters_in_resource(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*abc"}]), True)

    def test_no_asterisk_in_resource(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "arn:aws:iam::123456789012:role/role-name"}]), True)

    def test_lack_of_effect(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Action": ["iam:ListRoles", "iam:ListUsers"], "Resource": "*"}]), True)

    def test_lack_of_resource(self):
        self.assertEqual(aws_json.verify_list_of_statements([{"Effect": "Allow", "Action": ["iam:ListRoles", "iam:ListUsers"]}]), True)

def run_tests():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestInvalidInput))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCorrectInput))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestAbsolutePath))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestJsonString))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestPolicyName))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestStatement))

if __name__ == '__main__':
    aws_json.set_debug_mode(True)
    unittest.main()