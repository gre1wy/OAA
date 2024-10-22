import re

# разбиваем ввод на слова лексером
# парсером обрабатываем слова

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
    
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Invalid in lexer')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_token_type(self, token):
        """Determine the token type based on the token value."""
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

        # Check for each pattern
        for pattern, token_type in token_patterns.items():
            if re.match(pattern, token, re.IGNORECASE if token_type in ['CREATE', 'INSERT', 'PRINT_INDEX', 'SEARCH', 'WHERE'] else 0):
                return token_type

        self.error()

    def tokenize_text(self, text):
        words = re.findall(r'[a-zA-Z0-9_]+', text)
        return words

    def get_next_token(self):
        """Get the next token from the input, handling quoted strings and other token types."""
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # End of command
            if self.current_char == ';':
                self.advance()
                return Token('EOI', ';')

            # Handle the minus sign
            if self.current_char == '-':
                self.advance()
                return Token('MIN', '-')

            # Initialize result for gathering token characters
            result = ''

            # Handle quoted strings (documents or words)
            if self.current_char == '"':
                self.advance()
                result, contains_space = self._get_quoted_string()
                token_type = 'DOCUMENT' if contains_space else 'WORD'
                result = self.tokenize_text(result)
                return Token(token_type, result)

            # Handle angle brackets for <N>
            if self.current_char == '<':
                self.advance()
                result = self._get_angle_bracket_content()
                if result.isdigit():
                    return Token('DIST', int(result))  # Return as an integer
                else:
                    self.error()  # Error if not a number

            # Gather ordinary words/identifiers
            while self.current_char is not None and not self.current_char.isspace() and self.current_char not in [';', '"']:
                result += self.current_char
                self.advance()

            if result:
                token_type = self.get_token_type(result)
                return Token(token_type, result)

        return Token('EOF', None)

    def _get_quoted_string(self):
        """Helper method to handle quoted strings and determine if they contain spaces."""
        result = ''
        contains_space = False
        while self.current_char is not None and self.current_char != '"':
            if self.current_char.isspace():
                contains_space = True
            result += self.current_char
            self.advance()

        # Если мы достигли конца текста без закрывающей кавычки, вызываем ошибку
        if self.current_char is None:
            self.error()  # Незакрытая кавычка

        self.advance()  # Move past the closing quote
        return result, contains_space

    def _get_angle_bracket_content(self):
        """Helper method to gather content inside angle brackets."""
        result = ''
        while self.current_char is not None and self.current_char != '>':
            result += self.current_char
            self.advance()

        # Если мы достигли конца текста без закрывающей угловой скобки, вызываем ошибку
        if self.current_char is None:
            self.error()  # Незакрытая угловая скобка

        self.advance()  # Move past the closing bracket
        return result



# поработать с не закрывающимся кавычками

if __name__ == '__main__':
    lexer = Lexer('CREATE \t \r one_piece;')

    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()
