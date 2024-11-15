from lexer import Lexer
from parser import Parser
from invertedIndex import DB
import sys
def main():
    print("Welcome to the text collection management system!")
    print("You can use the following commands:")
    print("  CREATE <collection_name>;")
    print("  INSERT <collection_name> \"<document>\";")
    print("  PRINT_INDEX <collection_name>;")
    print("  SEARCH <collection_name> WHERE \"<word>\" [<N> \"<word>\"];")
    print("Type '-q' to quit.")
    
    db = DB()

    while True:
        try:
            # Accepting command from the user
            # text = input('Enter command: ')
            text = sys.stdin.read()
            # Exit if user types '-q'
            if text.strip().lower() == '-q':
                print("Exiting the system.")
                break
            
            # Creating a lexer instance
            lexer = Lexer(text)
            
            # Creating a parser instance, passing db
            parser = Parser(lexer, db)
            
            # Calling auto_parse which does all the magic
            parser.auto_parse()
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
    

