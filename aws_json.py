import json

# I understand that in all cases, except of valid AWS::IAM::Role Policy data with asterisk (*) in 'Resource' field, the program will return True,
# including cases with wrong data format.

def additional_keys_exist(input_map, listed_keys):
    return any(key not in listed_keys for key in input_map.keys())

def verify_aws_json_format(json_data):

    if "PolicyName" not in json_data:
        print("Invalid AWS::IAM::Role Policy: lack of PolicyName")
        return True
    
    if "PolicyDocument" not in json_data:
        print("Invalid AWS::IAM::Role Policy: lack of PolicyDocument")
        return True
    
    policy_document = json_data["PolicyDocument"]

    if "Statement" not in policy_document.keys():
        print("Invalid AWS::IAM::Role Policy: lack of Statement")
        return True
    
    list_of_statements = policy_document["Statement"]
    map_of_statements = list_of_statements[0]

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