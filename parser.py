from lexer import Lexer
from invertedIndex import DB

class Parser(object):

    """
    Parser for processing commands from the lexer and executing actions in the database.
    This class interprets tokenized input and performs the corresponding operations.
    """

    def __init__(self, lexer, db):
        
        self.lexer = lexer 
        self.db = db
        self.current_token = self.lexer.get_next_token()

    def error(self):

        raise Exception('Invalid syntax')

    def eat(self, token_type, token_type_second=None):

        """Checks if the current token type matches the expected type. If so, it moves 
        to the next token. If two types are provided, it checks one of them.


        token_type: expected token type
        token_type_second: additional token type for checking (optional)
        """
    
        if self.current_token.type == token_type or (token_type_second and self.current_token.type == token_type_second):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse_create(self):

        """Parses the CREATE command"""

        #('CREATE', 'create')
        self.eat('CREATE')
        #('COLLECTION', 'hello')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION') 
        #('EOI', ';')
        self.eat('EOI') 
        print(f"Creating collection: {collection_name}")
        return collection_name

    def parse_insert(self):

        """Parses the INSERT command"""

        self.eat('INSERT')  
        collection_name = self.current_token.value 
        self.eat('COLLECTION')  
        document = self.current_token.value 
        self.eat('DOCUMENT', 'WORD')  
        self.eat('EOI')  
        print(f"Inserting in {collection_name} document: {document}")
        return collection_name, document
    
    def parse_print_index(self): 

        """Parses the PRINT_INDEX command"""

        self.eat('PRINT_INDEX')  
        collection_name = self.current_token.value  
        self.eat('COLLECTION')  
        self.eat('EOI')  
        print(f"Printing index in collection: {collection_name}")
        return collection_name
    
    def parse_search(self):

        """Parses the SEARCH command"""

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
                return collection_name, word1[0], word2[0], None
            
            
            if self.current_token.type == 'DIST': # WHERE “keyword_1” <N> “keyword_2” 
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

        """Automatically parses the command based on the token type"""

        command_type = self.current_token.type

        if command_type == 'CREATE':
            collection_name = self.parse_create()
            self.db.create_collection(collection_name) 
            return  collection_name
            
        elif command_type == 'INSERT':
            collection_name, document = self.parse_insert()
            self.db.insert_document(collection_name, document)
            return  collection_name, document
            
        elif command_type == 'PRINT_INDEX':
            collection_name = self.parse_print_index()
            self.db.print_index(collection_name)
            return collection_name  

        elif command_type == 'SEARCH':
            collection_name, word1, word2, dist = self.parse_search()
            if collection_name and word1 and word2 and dist:
                self.db.search_distance(collection_name, word1, word2, dist)
                return collection_name, word1, word2, dist

            elif collection_name and word1 and word2 and not dist:
                self.db.search_range(collection_name, word1, word2)
                return collection_name, word1, word2, dist

            elif collection_name and word1 and not word2 and not dist:
                self.db.search_word(collection_name, word1)
                return collection_name, word1, word2, dist

            elif collection_name and not word1 and not word2 and not dist:
                self.db.search(collection_name)
                return collection_name, word1, word2, dist
        else:
            self.error() 




 # type: ignore