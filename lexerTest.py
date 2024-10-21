from lexer import Lexer

class TestLexer:
    def __init__(self):
        self.test_cases = [
            # Valid commands
            ('CREATE my_collection;', [('CREATE', 'CREATE'), ('COLLECTION', 'my_collection'), ('EOI', ';')]),
            ('INSERT my_collection "This is a test document";', [('INSERT', 'INSERT'), ('COLLECTION', 'my_collection'), ('DOCUMENT', 'This is a test document'), ('EOI', ';')]),
            ('PRINT_INDEX my_collection;', [('PRINT_INDEX', 'PRINT_INDEX'), ('COLLECTION', 'my_collection'), ('EOI', ';')]),
            ('SEARCH my_collection WHERE "word";', [('SEARCH', 'SEARCH'), ('COLLECTION', 'my_collection'), ('WHERE', 'WHERE'), ('WORD', 'word'), ('EOI', ';')]),
 '''???'''           ('SEARCH my_collection WHERE "start" - "end";', [('SEARCH', 'SEARCH'), ('COLLECTION', 'my_collection'), ('WHERE', 'WHERE'), ('WORD', 'start'), ('MIN', '-'), ('WORD', 'end'), ('EOI', ';')]),
 '''???'''           ('SEARCH my_collection WHERE "word" <2> "another";', [('SEARCH', 'SEARCH'), ('COLLECTION', 'my_collection'), ('WHERE', 'WHERE'), ('WORD', 'word'), ('DIST', 2), ('WORD', 'another'), ('EOI', ';')]),
            
            # Handling spaces
            ('   CREATE   collection_name   ;   ', [('CREATE', 'CREATE'), ('COLLECTION', 'collection_name'), ('EOI', ';')]),

            # Testing with quoted strings containing spaces ??????
            ('INSERT my_collection "This is a document with spaces";', [('INSERT', 'INSERT'), ('COLLECTION', 'my_collection'), ('DOCUMENT', 'This is a document with spaces'), ('EOI', ';')]),

            # Handling invalid commands
            ('INVALID COMMAND;', None),  # This should raise an error ???????
            ('CREATE 123invalid_name;', None),  # Invalid collection name
            ('INSERT my_collection "Missing closing quote;', None),  # Missing closing quote
            ('SEARCH my_collection WHERE "word" <non-numeric>;', None),  # Invalid distance value
        ]

    def test_lexer(self, input_text):
        lexer = Lexer(input_text)
        tokens = []
        
        token = lexer.get_next_token()
        while token.type != 'EOF':
            tokens.append(token)
            token = lexer.get_next_token()
        
        return tokens

    def run_tests(self):
        for test_input, expected_output in self.test_cases:
            print(f'Testing input: {test_input}')
            try:
                tokens = self.test_lexer(test_input)
                if expected_output is None:
                    print('Expected an error but got tokens instead:', tokens)
                else:
                    print('Tokens:', [(token.type, token.value) for token in tokens])
                    assert [(token.type, token.value) for token in tokens] == expected_output, "Mismatch in expected tokens"
                print('---')
            except Exception as e:
                if expected_output is None:
                    print(f'Error as expected: {e}')
                else:
                    print(f'Unexpected error: {e}')
                print('---')

if __name__ == '__main__':
    tester = TestLexer()
    tester.run_tests()

