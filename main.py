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
            # Принимаем команду от пользователя
            text = input('Enter command: ')
            
            # Выход, если пользователь ввел 'exit'
            if text.lower() == '-q':
                print("Exiting the system.")
                break
            
            # Создаем экземпляр лексера
            lexer = Lexer(text)
            
            # Создаем экземпляр парсера с передачей db
            parser = Parser(lexer, db)
            
            # Вызываем авто-парсер, который делает всю магию
            parser.auto_parse()
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
    

