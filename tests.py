import unittest
import json
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

    # def test_resource_with_asterisk_many_resources(self):
    #     self.assertEqual(verify_json_input("tests/valid_json/example_with_asterisk_certain_resource.json"), False)

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
 

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()