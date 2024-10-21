from lexer import Lexer
from parser import Parser
from invertedIndex import DB

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
            # Приймаємо команду від користувача
            text = input('Enter command: ')
            
            # Вихід, якщо користувач ввів '-q'
            if text.lower() == '-q':
                print("Exiting the system.")
                break
            
            # Створюємо екземляр лексера
            lexer = Lexer(text)
            
            # Створюємо екземляр парсера, передаючи лексер і бд
            parser = Parser(lexer, db)
            
            # Викликаєм авто-парсер, який робить всю магію
            parser.auto_parse()
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
    

