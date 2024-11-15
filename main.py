from lexer import Lexer
from parser import Parser
from invertedIndex import DB
import sys

def execute_file_commands(filename, db):
    """Executes commands from a given file"""
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    print(f"Command: {line.strip()}")
                    lexer = Lexer(line)
                    parser = Parser(lexer, db)
                    parser.auto_parse()
    except Exception as e:
        print(f"Error while executing commands from file: {e}")

def main():
    print("Welcome to the text collection management system!")
    print("You can execute commands interactively or from a file.")
    print("Type '-q' to quit.")
    print("To execute commands from a file, use: `file <filename>`")

    db = DB()

    while True:
        try:
            text = sys.stdin.read()
            if text.strip().lower() == '-q':
                print("Exiting the system.")
                break

            # Execute commands from a file
            if text.startswith('file '):
                filename = text.split(' ', 1)[1]
                execute_file_commands(filename, db)
                continue

            # Process single command
            lexer = Lexer(text)
            parser = Parser(lexer, db)
            parser.auto_parse()

        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
