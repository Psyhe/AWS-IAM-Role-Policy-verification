import json
import re

DEBUG = False

# I understand that in all cases, except for valid AWS::IAM::Role Policy data with an asterisk (*) in the 'Resource' field, 
# the program will return True, including cases with incorrect data formats.

def debug_print(s):
    if DEBUG:
        print(s)

def check_requirements_for_statement(data):
    map_of_statements = data

    obligatory_keys = ["Effect", "Action", "Resource"]

    optional_keys = ["Sid", "Principal", "Condition", "Resource"]

    for key in obligatory_keys:
        if key not in map_of_statements.keys():
            debug_print("Lack of obligatory field: " + key)
            return False
    
    if additional_keys_exist(map_of_statements, obligatory_keys + optional_keys):
        debug_print("Invalid AWS::IAM::Role Policy: wrong data format")
        return False
    
    if map_of_statements["Effect"] not in ["Allow", "Deny"]:
        debug_print("Invalid AWS::IAM::Role Policy: wrong Effect format")
        return False
    
    if type(map_of_statements["Action"]) is not list:
        debug_print("Invalid AWS::IAM::Role Policy: wrong Action format")
        return False
    
    return True


def check_if_asterisk_in_resource(data):
    if data == "*":
        return False
    else:
        if type(data) is not list:
            debug_print("Invalid AWS::IAM::Role Policy: wrong Resource format")
            return True
        else:
            debug_print("Lack of asterisk (*) in 'Resource' field.")
            return True
    
def verify_list_of_statements(list_of_statements):
    if type(list_of_statements) is not list:
        debug_print("Invalid AWS::IAM::Role Policy: wrong Statement format")
        return True
    
    answer = True
    
    for statement in list_of_statements:
        if check_requirements_for_statement(statement) == False:
            return True
        else: 
            resource = statement["Resource"]
            if check_if_asterisk_in_resource(resource) == False:
                # There might be error later which would result in True
                answer =  False

    return answer

def additional_keys_exist(input_map, listed_keys):
    return any(key not in listed_keys for key in input_map.keys())

def check_pattern(pattern, s):
    if re.fullmatch(pattern, s):
        return True
    else:
        return False
    
def verify_policy_name_properties(policy_name):
    if not (check_pattern(r"[\w+=,.@-]+", policy_name)):
        debug_print("Invalid AWS::IAM::Role Policy: wrong PolicyName format")
        return True
    
    if len(policy_name) > 128:
        debug_print("Invalid AWS::IAM::Role Policy: PolicyName is too long")
        return True
    
    return False

def is_dict(s):
    if type(s) is dict:
        return True
    else:
        return False

def verify_aws_json_format(json_data):

    if "PolicyName" not in json_data:
        debug_print("Invalid AWS::IAM::Role Policy: lack of PolicyName")
        return True
    
    if "PolicyDocument" not in json_data:
        debug_print("Invalid AWS::IAM::Role Policy: lack of PolicyDocument")
        return True
    
    if len(json_data.keys()) > 2:
        debug_print("Invalid AWS::IAM::Role Policy: too many properties in JSON file")
        return True
    
    if verify_policy_name_properties(json_data["PolicyName"]):
        return True
    
    policy_document = json_data["PolicyDocument"]

    if is_dict(policy_document) == False:
        debug_print("Invalid AWS::IAM::Role Policy: wrong PolicyDocument format")
        return True
    
    if additional_keys_exist(policy_document, ["Version", "Statement"]):
        debug_print("Invalid AWS::IAM::Role Policy: wrong PolicyDocument format - additional unrequired information")
        return True
    
    if "Version" not in policy_document.keys() or "Statement" not in policy_document.keys():
        debug_print("Invalid AWS::IAM::Role Policy: lack of Version or Statement")
        return True
    
    list_of_statements = policy_document["Statement"]

    if verify_list_of_statements(list_of_statements) == False:
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
        debug_print("File not found. Please try again.")
        debug_print(path_to_file)
        return True
    except Exception as e:
        debug_print(f"An error occurred: {e}")
        return True
    
def set_debug_mode(mode):
    global DEBUG
    DEBUG = mode
    
if __name__ == "__main__":
    set_debug_mode()
    verify_json_input("tests/json_example.json")