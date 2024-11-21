import re # For processing regular expressions

class Token(object):

    """
    Class for representing tokens.
    Each token has a type (e.g., CREATE, WORD) and a value.
    """

    def __init__(self, type, value):

        self.type = type
        self.value = value

    def __str__(self):

        """Returns the string representation of the token"""

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):

        """Returns the representation of the token"""

        return self.__str__()
    
class Lexer(object):

    """
    Class for tokenizing text.
    Splits input text into tokens to be processed by the parser.
    """

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Error in lexer')

    def advance(self):

        """Moves the `pos` pointer and sets the `current_char` variable"""

        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # Indicates the end of the input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):

        """Skips whitespace"""

        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_token_type(self, token):

        """Determines the token type based on its value using regular expressions"""
        
        token_patterns = {
            r'CREATE': 'CREATE',
            r'INSERT': 'INSERT',
            r'PRINT_INDEX': 'PRINT_INDEX',
            r'SEARCH': 'SEARCH',
            r'WHERE': 'WHERE',
            r'^[a-zA-Z][a-zA-Z0-9_]*$': 'COLLECTION',
            r'^"[a-zA-Z][a-zA-Z0-9_]*"$': 'WORD', 
            r'^".*"$': 'DOCUMENT',
            r'^-': 'MIN',
            r'^<\d+>$': 'DIST',
            r'^;$': 'EOI',
            r'.+': 'JUNK'
        }

        # Check which pattern the token matches
        for pattern, token_type in token_patterns.items():
            if re.match(pattern, token, re.IGNORECASE if token_type in ['CREATE', 'INSERT', 'PRINT_INDEX', 'SEARCH', 'WHERE'] else 0):
                return token_type

        self.error()

    def tokenize_text(self, text):

        """Splits the text into individual words using regular expressions"""
        
        words = re.findall(r'[a-zA-Z0-9_]+', text)
        return words

    def get_next_token(self):

        """Retrieves the next token from the input.
        Handles quoted strings, angle brackets, and regular words."""
        
        while self.current_char is not None:


            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == ';':
                self.advance()
                return Token('EOI', ';')

            if self.current_char == '-':
                self.advance()
                return Token('MIN', '-')

            result = ''  # To store the token value

            if self.current_char == '"':
                self.advance()
                result, contains_space = self._get_quoted_string()
                token_type = 'DOCUMENT' if contains_space else 'WORD'
                result = self.tokenize_text(result)
                return Token(token_type, result)

            if self.current_char == '<':
                self.advance()
                result = self._get_angle_bracket_content()
                if result.isdigit():
                    return Token('DIST', int(result))  
                else:
                    self.error()  # Error if not a number

            # Collecting regular words/identifiers
            while self.current_char is not None and not self.current_char.isspace() and self.current_char not in [';', '"']:
                result += self.current_char
                self.advance()

            if result:
                token_type = self.get_token_type(result)
                return Token(token_type, result)

        return Token('EOF', None)

    def _get_quoted_string(self):

        """Helper method for processing quoted strings and determining if they contain spaces """
        
        result = ''
        contains_space = False
        while self.current_char is not None and self.current_char != '"':
            if self.current_char.isspace():
                contains_space = True
            result += self.current_char
            self.advance()

        if self.current_char is None:
            self.error()  # Unclosed quote

        self.advance() 
        return result, contains_space

    def _get_angle_bracket_content(self):

        """Helper method for collecting content in angle brackets"""
        
        result = ''
        while self.current_char is not None and self.current_char != '>':
            result += self.current_char
            self.advance()

        if self.current_char is None:
            self.error()  # Unclosed angle bracket

        self.advance()  
        return result


if __name__ == '__main__':
    lexer = Lexer('CREATE one_piece;')
    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()