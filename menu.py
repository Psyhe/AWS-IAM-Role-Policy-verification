from tests import run_tests
from aws_json import verify_json_input
from aws_json import set_debug_mode

def run_program():
    path = input("Enter the path of the file: ")
    print(verify_json_input(path))

def write_answer(acceptable_set):
    answer = input()
    
    if answer in acceptable_set:
        return answer
    else:
        print("Invalid input. Please try again.")
        return write_answer(acceptable_set)
    
def if_debug_mode():
    print("Do you want to set debug mode? (yes/no)")
    debug_choice = write_answer(["yes", "no"])
    if debug_choice == "yes":
        set_debug_mode(True)
        print("Setting debug mode...")

def menu():
    print("What do you want to do?")
    print("Run the program: write 'run'")
    print("Test program: write 'test'")
    print("Exit program: write 'exit'")
    print("Write your choice below:")

    choice = write_answer(["run", "test", "exit"])

    if choice == "run":
        if_debug_mode()
        print("Running program...")
        run_program()
    elif choice == "test":
        if_debug_mode()
        print("Testing program...")
        run_tests()
    elif choice == "exit":
        print("Exiting program...")


if __name__ == "__main__":
    menu()