from lexer import Lexer

class Parser(object):
    def __init__(self, Lexer):
        self.lexer = Lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type, token_type_second=None):
        """Сравниваем текущий токен с ожидаемым типом. Если тип совпадает, получаем следующий токен.
        Если переданы два типа, проверяем соответствие любому из них."""
        if self.current_token.type == token_type or (token_type_second and self.current_token.type == token_type_second):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse_create(self):
        """Парсим команду CREATE."""
        self.eat('CREATE')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION')  
        self.eat('EOI') 
        print(f"Creating collection: {collection_name}")
        # create collection
        return collection_name

    def parse_insert(self):
        """Парсим команду INSERT."""
        self.eat('INSERT')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION')  
        document = self.current_token.value 
        self.eat('DOCUMENT', 'WORD')  
        self.eat('EOI')  
        print(f"Inserting in {collection_name} document: {document}")
        # insert document
        return collection_name, document
    
    def parse_print_index(self): 
        """Парсим команду print_index."""
        self.eat('PRINT_INDEX')  
        collection_name = self.current_token.value  
        self.eat('COLLECTION')  
        self.eat('EOI')  
        print(f"Printing index in collection: {collection_name}")
        # print index for collection
        return collection_name
    
    def parse_search(self):
        """Парсим команду SEARCH."""
        self.eat('SEARCH')  
        collection_name = self.current_token.value  
        self.eat('COLLECTION')  

        if self.current_token.type == 'WHERE': # WHERE “keyword”
            self.eat('WHERE')
            word1 = self.current_token.value  
            self.eat('WORD')  

            if self.current_token.type == 'MIN':  # WHERE “keyword_1” - “keyword_1”
                self.eat('MIN')
                word2 = self.current_token.value
                self.eat('WORD')
                self.eat('EOI')  
                print(f"Searching in collection {collection_name} for documents with word between '{word1}' and '{word2}'")
                return collection_name, word1, '-', word2
            
            if self.current_token.type == 'DIST': # “keyword_1” <N> “keyword_2” 
                dist = self.current_token.value
                self.eat('DIST')
                word2 = self.current_token.value
                self.eat('WORD')
                self.eat('EOI')  
                print(f"Searching in collection {collection_name} for documents with word on distance {dist} between '{word1}' and '{word2}'")
                return collection_name, word1, dist, word2
            
            self.eat('EOI') 
            print(f"Searching in collection {collection_name} for documents with word '{word1}'")
            return collection_name, word1
        
        self.eat('EOI')  
        print(f"Searching all documents in collection: {collection_name}")
        return collection_name
    
    def auto_parse(self):
        """Автоматически определяем и парсим команду."""
        command_type = self.current_token.type

        if command_type == 'CREATE':
            return self.parse_create()
        elif command_type == 'INSERT':
            return self.parse_insert()
        elif command_type == 'PRINT_INDEX':
            return self.parse_print_index()
        elif command_type == 'SEARCH':
            return self.parse_search()
        else:
            self.error()


