## AWS IAM Role Policy Verifier

### Overview
This project verifies AWS IAM Role Policy JSON data. It returns logical false if an input JSON Resource field contains a single asterisk and true in any other case. If any error or invalid input occurs, the result is also true, and the reason is printed if debug mode is on.

### Assumptions
- The JSON must contain exactly two keys: "PolicyName" and "PolicyDocument", as defined in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html).
- I assumed that no additional keys are allowed, because I chose to stick to spectification from provided [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html) but
it might need to be changed according to [this information](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html)
- Valid and invalid structures of PolicyDocument are considered according to the [AWS IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json).
- Fields "Statement" and "Version" are assumed to be mandatory.
- Fields "Effect" and "Action" are considered compulsory as they are not marked as "optional" or "required in only some circumstances"
- Field "Resource" is compulsory as it needs to exists to contain single asterisk.

### Usage
To run and manage the project:
1. Type `python3 main.py`.
2. The menu will display in the console, and users can choose what to do.
    - Type 'exit' to end the program.
    - Type 'test', then choose whether to turn on debug mode ('yes' or 'no') to run tests.
    - Type 'run', then choose whether to turn on debug mode ('yes' or 'no'), then type the path to the file you want to verify.
3. Import `verify_json_input` from `aws_json.py` and pass the path to the JSON file as an argument to use the function in your code.
    - If you want to see debug info (and understand why the answer is True), import function `set_mode` and pass True as an argument.
4. To run test cases, type `python3 tests.py` in the console.

Folder 'tests' contains folders with various json input files, also invalid ones.