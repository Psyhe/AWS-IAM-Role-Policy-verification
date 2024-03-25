from test import run_tests
from aws_json import verify_json_input

def run_program():
    path = input("Enter the path of the file: ")
    print(verify_json_input(path))

def write_answer():
    answer = input()
    
    if answer == "run" or answer == "test" or answer == "exit":
        return answer
    else:
        print("Invalid input. Please try again.")
        return write_answer()

def menu():
    print("What do you want to do?")
    print("Run the program: write 'run'")
    print("Test program: write 'test'")
    print("Exit program: write 'exit'")
    print("Write your choice below:")

    choice = write_answer()

    if choice == "run":
        print("Running program...")
        run_program()
    elif choice == "test":
        print("Testing program...")
        run_tests()
    elif choice == "exit":
        print("Exiting program...")


if __name__ == "__main__":
    menu()