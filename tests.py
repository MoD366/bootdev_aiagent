from functions.run_python import *


def main():
    print(run_python_file("calculator", "main.py") + "\n")
    print(run_python_file("calculator", "main.py", ["3 + 5"]) + "\n")
    print(run_python_file("calculator", "tests.py") + "\n")
    print(run_python_file("calculator", "../main.py") + "\n")
    print(run_python_file("calculator", "nonexistent.py"))

main()