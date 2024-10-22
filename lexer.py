import re # For processing regular expressions

class Token(object):

    """Class for representing tokens"""

    def __init__(self, type, value):

        """Initialization of the token

        Args:
            type (str): Type of the token
            value (str): Value of the token
        """

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

    """Class for tokenizing text

    Used to split the input text into tokens,
    which can then be processed by the parser
    """

    def __init__(self, text):

        """Initialization of the lexer

        Args:
            text (str): Text for tokenization
        """

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
            r'^;$': 'EOI'
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

        """Gets the next token from the input, processing quoted strings and other types of tokens"""
        
        while self.current_char is not None:

            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # End of command
            if self.current_char == ';':
                self.advance()
                return Token('EOI', ';')

            # Processing the minus sign
            if self.current_char == '-':
                self.advance()
                return Token('MIN', '-')

            # Initialize result for collecting token characters
            result = ''

            # Processing quoted strings (documents or words)
            if self.current_char == '"':
                self.advance()
                result, contains_space = self._get_quoted_string()
                token_type = 'DOCUMENT' if contains_space else 'WORD'
                result = self.tokenize_text(result)
                return Token(token_type, result)

            # Processing angle brackets for <N>
            if self.current_char == '<':
                self.advance()
                result = self._get_angle_bracket_content()
                if result.isdigit():
                    return Token('DIST', int(result))  # Return as an integer
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

        # If reached the end of the text without a closing quote, raise an error
        if self.current_char is None:
            self.error()  # Unclosed quote

        self.advance()  # Move past the closing quote
        return result, contains_space

    def _get_angle_bracket_content(self):

        """Helper method for collecting content in angle brackets"""
        
        result = ''
        while self.current_char is not None and self.current_char != '>':
            result += self.current_char
            self.advance()

        # If reached the end of the text without a closing angle bracket, raise an error
        if self.current_char is None:
            self.error()  # Unclosed angle bracket

        self.advance()  # Move past the closing bracket
        return result



if __name__ == '__main__':
    lexer = Lexer('CrEate "jje"fkfo; <4>')

    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()
