import re

# разбиваем ввод на слова лексером
# парсером обрабатываем слова

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance."""
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
        raise Exception('Invalid character')

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
        if re.match(r'CREATE', token, re.IGNORECASE):
            return 'CREATE'
        elif re.match(r'INSERT', token, re.IGNORECASE):
            return 'INSERT'
        elif re.match(r'PRINT_INDEX', token, re.IGNORECASE):
            return 'PRINT_INDEX'
        elif re.match(r'SEARCH', token, re.IGNORECASE):
            return 'SEARCH'
        elif re.match(r'WHERE', token, re.IGNORECASE):
            return 'WHERE'
        elif re.match(r'[a-zA-Z][a-zA-Z0-9_]*', token):
            return 'COLLECTION'
        elif re.match(r'^"[a-zA-Z][a-zA-Z0-9_]*"$', token):
            return 'WORD'
        elif re.match(r'^".*"$', token):
            return 'DOCUMENT'
        elif token == '-':
            return 'MIN'
        elif re.match(r'^<\d+>$', token):
            return 'DIST'
        elif token == ';':
            return 'EOI'
        else:
            self.error()

    def get_next_token(self):
        """Get the next token from the input, handling quoted strings and other token types."""
        while self.current_char is not None:

            # Пропускаем пробелы
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Проверяем на конец команды
            if self.current_char == ';':
                self.advance()
                return Token('EOI', ';')

            # Проверяем на минус (например, для диапазонов)
            if self.current_char == '-':
                self.advance()
                return Token('MIN', '-')

            result = ''

            # Проверяем на открытые кавычки для документов или строк
            if self.current_char == '"':
                self.advance()  # Пропускаем начальную кавычку
                contains_space = False
                while self.current_char is not None and self.current_char != '"':
                    if self.current_char.isspace():
                        contains_space = True  # Отмечаем, что внутри есть пробел
                    result += self.current_char
                    self.advance()
                self.advance()  # Пропускаем закрывающую кавычку
                if contains_space:
                    return Token('DOCUMENT', result)  # Если есть пробелы, возвращаем DOCUMENT
                else:
                    return Token('WORD', result)  # Если нет пробелов, возвращаем WORD

            # Проверяем на угловые скобки для числовых значений (например, "<N>")
            if self.current_char == '<':
                self.advance()  # Пропускаем начальную угловую скобку
                while self.current_char is not None and self.current_char != '>':
                    result += self.current_char
                    self.advance()
                self.advance()  # Пропускаем закрывающую угловую скобку
                # Проверяем, что результат — это целое число
                if result.isdigit():
                    return Token('DIST', int(result))  # Возвращаем целое значение
                else:
                    self.error()  # Если внутри угловых скобок не число, генерируем ошибку

            # Собираем обычные слова/идентификаторы
            while self.current_char is not None and not self.current_char.isspace() and self.current_char != ';' and self.current_char != '"':
                result += self.current_char
                self.advance()

            if result:
                token_type = self.get_token_type(result)
                return Token(token_type, result)

        return Token('EOF', None)



if __name__ == '__main__':
    lexer = Lexer('CrEate jjefkfo; <ter>')

    token = lexer.get_next_token()
    while token.type != 'EOF':
        print(token)
        token = lexer.get_next_token()
