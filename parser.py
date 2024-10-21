from lexer import Lexer
from invertedIndex import DB

class Parser(object):

    """Парсер для обробки команд з лексера та виконання дій у базі даних"""

    def __init__(self, Lexer, db):

        """Ініціалізує парсер з лексером та базою даних

        Args:
            lexer (Lexer): лексер, що відповідає за токенізацію тексту
            db (DB): об'єкт бази даних для виконання команд
        """
    
        self.lexer = Lexer
        self.db = db
        self.current_token = self.lexer.get_next_token()

    def error(self):

        """Викликає помилку синтаксису"""

        raise Exception('Invalid syntax')

    def eat(self, token_type, token_type_second=None):

        """Перевіряє чи тип поточного токена відповідає очікуваному типу. Якщо так, то переходимо 
        на наступний токен. Якщо передані 2 типи, перевіряєму відповідність будь-якому з них (?)

        Args:
            token_type (str): Очікуваний тип токена
            token_type_second (str): Додатковий тип токена для перевірки (необов'язково)
        """
    
        if self.current_token.type == token_type or (token_type_second and self.current_token.type == token_type_second):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse_create(self):

        """Парсить команду CREATE"""

        self.eat('CREATE')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION')  
        self.eat('EOI') 
        print(f"Creating collection: {collection_name}")
        return collection_name

    def parse_insert(self):

        """Парсить команду INSERT"""

        self.eat('INSERT')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION')  
        document = self.current_token.value 
        self.eat('DOCUMENT', 'WORD')  
        self.eat('EOI')  
        print(f"Inserting in {collection_name} document: {document}")
        return collection_name, document
    
    def parse_print_index(self): 

        """Парсить команду print_index"""

        self.eat('PRINT_INDEX')  
        collection_name = self.current_token.value  
        self.eat('COLLECTION')  
        self.eat('EOI')  
        print(f"Printing index in collection: {collection_name}")
        return collection_name
    
    def parse_search(self):

        """Парсить команду SEARCH"""

        self.eat('SEARCH')  
        collection_name = self.current_token.value  
        self.eat('COLLECTION')  

        if self.current_token.type == 'WHERE': # WHERE “keyword”
            self.eat('WHERE')
            word1 = self.current_token.value  
            self.eat('WORD')  

            # Перевірка на використання мінуса (-) для пошуку у діапазоні
            if self.current_token.type == 'MIN':  # WHERE “keyword_1” - “keyword_1”
                self.eat('MIN')
                word2 = self.current_token.value
                self.eat('WORD')
                self.eat('EOI')  
                print(f"Searching in collection {collection_name} for documents with word between '{word1}' and '{word2}'")
                return collection_name, word1[0], word2[0], None
            
            # Перевірка на відстань між словами
            if self.current_token.type == 'DIST': # “keyword_1” <N> “keyword_2” 
                dist = self.current_token.value
                self.eat('DIST')
                word2 = self.current_token.value
                self.eat('WORD')
                self.eat('EOI')  
                print(f"Searching in collection {collection_name} for documents with word on distance {dist} between '{word1}' and '{word2}'")
                return collection_name, word1[0], word2[0], dist
            
            self.eat('EOI') 

            print(f"Searching in collection {collection_name} for documents with word '{word1}'")
            return collection_name, word1[0], None, None
        
        self.eat('EOI')  

        print(f"Searching all documents in collection: {collection_name}")
        return collection_name, None, None, None
    
    def auto_parse(self):

        """Автоматично парсить команду на основі типу токена"""

        command_type = self.current_token.type

        # Обробка команд на основі типу токена
        if command_type == 'CREATE':
            collection_name = self.parse_create()
            self.db.create_collection(collection_name)  
            
        elif command_type == 'INSERT':
            collection_name, document = self.parse_insert()
            self.db.insert_document(collection_name, document)  
            
        elif command_type == 'PRINT_INDEX':
            collection_name = self.parse_print_index()
            self.db.print_index(collection_name)  

        elif command_type == 'SEARCH':
            collection_name, word1, word2, dist = self.parse_search()
            if collection_name and word1 and word2 and dist:
                self.db.search_distance(collection_name, word1, word2, dist) 

            elif collection_name and word1 and word2 and not dist:
                self.db.search_range(collection_name, word1, word2)  

            elif collection_name and word1 and not word2 and not dist:
                self.db.search_word(collection_name, word1)  

            elif collection_name and not word1 and not word2 and not dist:
                self.db.search(collection_name)  
        else:
            self.error() # Генерує помилку для невідомої команди




 # type: ignore