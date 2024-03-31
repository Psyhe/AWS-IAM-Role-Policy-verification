import json
import re

# I understand that in all cases, except of valid AWS::IAM::Role Policy data with asterisk (*) in 'Resource' field, the program will return True,
# including cases with wrong data format.

def check_if_asterisk_in_resource(data):
    map_of_statements = data

    obligatory_keys = ["Effect", "Action"]

    optional_keys = ["Sid", "Principal", "Condition", "Resource"]

    if "Resource" not in map_of_statements.keys():
        print("Lack of Resource field.")
        return True
    
    if additional_keys_exist(map_of_statements, obligatory_keys + optional_keys):
        print("Invalid AWS::IAM::Role Policy: wrong data format")
        return True
    
    data = map_of_statements["Resource"]

    if data == "*":
        return False
    else:
        print("Lack of asterisk (*) in 'Resource' field.")
        return True

def additional_keys_exist(input_map, listed_keys):
    return any(key not in listed_keys for key in input_map.keys())

def check_pattern(pattern, s):
    if re.fullmatch(pattern, s):
        return True
    else:
        return False
    
def verify_policy_name_properties(policy_name):
    if not (check_pattern(r"[\w+=,.@-]+", policy_name)):
        print("Invalid AWS::IAM::Role Policy: wrong PolicyName format")
        return True
    
    if len(policy_name) > 128:
        print("Invalid AWS::IAM::Role Policy: PolicyName is too long")
        return True
    
    return False

def is_dict(s):
    if type(s) is dict:
        return True
    else:
        return False

def verify_aws_json_format(json_data):

    if "PolicyName" not in json_data:
        print("Invalid AWS::IAM::Role Policy: lack of PolicyName")
        return True
    
    if "PolicyDocument" not in json_data:
        print("Invalid AWS::IAM::Role Policy: lack of PolicyDocument")
        return True
    
    if len(json_data.keys()) > 2:
        print("Invalid AWS::IAM::Role Policy: to many properties in JSON file")
        return True
    
    if verify_policy_name_properties(json_data["PolicyName"]):
        return True
    
    policy_document = json_data["PolicyDocument"]

    print(policy_document)
    print("policy document")

    if is_dict(policy_document) == False:
        print("Invalid AWS::IAM::Role Policy: wrong PolicyDocument format")
        return True
    
    if additional_keys_exist(policy_document, ["Version", "Statement"]):
        print("Invalid AWS::IAM::Role Policy: wrong PolicyDocument format - additional unrequired information")
        return True

    if "Statement" not in policy_document.keys():
        print("Invalid AWS::IAM::Role Policy: lack of Statement")
        return True
    
    list_of_statements = policy_document["Statement"]

    for statement in list_of_statements:
        if check_if_asterisk_in_resource(statement) == False:
            return False
    
    return True

def operations_on_json(json_data):
    json_data = json.loads(json_data.read())

    return (verify_aws_json_format(json_data))

def verify_json_input(path_to_file):
    try:
        with open(path_to_file, "r") as file:
            return operations_on_json(file)
    except FileNotFoundError:
        print("File not found. Please try again.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return True
    
if __name__ == "__main__":
    verify_json_input("tests/json_example.json")